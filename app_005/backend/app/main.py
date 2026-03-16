"""
Skin Lesion Classifier - FastAPI Backend
Melanoma detection utilizing ABCD rule
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import logging
from datetime import datetime
import asyncio
from app.ml.llm import DermatologistAssistant

# Initialize LLM
llm_derm = DermatologistAssistant()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Skin Lesion Classifier API",
    description="Melanoma risk assessment using ABCD rule",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    # Allow Frontend on Port 3005
    allow_origins=["http://localhost:3005", "http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LesionCharacteristics(BaseModel):
    asymmetry_score: float = Field(..., ge=0, le=10, description="0-10 Score")
    border_irregularity: float = Field(..., ge=0, le=10, description="0-10 Score")
    color_variation: int = Field(..., ge=1, le=6, description="Number of distinct colors")
    diameter_mm: float = Field(..., ge=0, le=100, description="Diameter in mm")
    evolution: bool = False

class PredictionResponse(BaseModel):
    risk_level: str
    confidence: float
    probability_distribution: Dict[str, float]
    timestamp: datetime

class AnalysisRequest(BaseModel):
    lesion_data: LesionCharacteristics
    prediction: str
    confidence: float

class AnalysisResponse(BaseModel):
    analysis: str

class AIModel:
    def __init__(self):
        self.name = "Melanoma ABCD Model"
        self.classes = ['Benign', 'Suspicious', 'Malignant']
        logger.info(f"{self.name} initialized")
    
    async def predict(self, lesion: LesionCharacteristics) -> Dict:
        await asyncio.sleep(0.1) 
        
        # ABCD Rule Simulation
        # Asymmetry (x1.3), Border (x0.1), Color (x0.5), Diameter (x0.5)
        # Note: This is an illustrative heuristic, not clinical TDP.
        score = 0
        score += lesion.asymmetry_score * 0.1
        score += lesion.border_irregularity * 0.1
        score += lesion.color_variation * 0.2
        if lesion.diameter_mm > 6: score += 0.3
        if lesion.evolution: score += 0.4
        
        # Normalize roughly
        score = min(score, 1.5) / 1.5
        
        if score < 0.4:
            prediction = "Benign"
            probs = {"Benign": 0.85, "Suspicious": 0.10, "Malignant": 0.05}
        elif score < 0.7:
            prediction = "Suspicious"
            probs = {"Benign": 0.20, "Suspicious": 0.60, "Malignant": 0.20}
        else:
            prediction = "Malignant"
            probs = {"Benign": 0.05, "Suspicious": 0.15, "Malignant": 0.80}
            
        return {
            "prediction": prediction,
            "confidence": probs[prediction], 
            "probabilities": probs
        }

model = AIModel()

@app.get("/")
async def root():
    return {"message": "Skin Lesion Classifier API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/api/v1/predict", response_model=PredictionResponse)
async def predict_risk(data: LesionCharacteristics):
    try:
        result = await model.predict(data)
        return PredictionResponse(
            risk_level=result["prediction"],
            confidence=result["confidence"],
            probability_distribution=result["probabilities"],
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Prediction Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analyze", response_model=AnalysisResponse)
async def analyze_risk(request: AnalysisRequest):
    try:
        l = request.lesion_data
        context_str = f"Asymmetry: {l.asymmetry_score}/10, Border: {l.border_irregularity}/10, Colors: {l.color_variation}, Diameter: {l.diameter_mm}mm, Evolving: {l.evolution}"
        
        analysis = llm_derm.analyze_lesion({
            "patient_context": context_str,
            "prediction": request.prediction,
            "confidence": request.confidence
        })
        return AnalysisResponse(analysis=analysis)
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
