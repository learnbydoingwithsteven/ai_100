"""
Patient Risk Stratification - FastAPI Backend
Hospital readmission prediction
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import logging
from datetime import datetime
import asyncio
from app.ml.llm import RiskAssessmentAssistant

# Initialize LLM
llm_assistant = RiskAssessmentAssistant()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Patient Risk Stratification API",
    description="Hospital readmission prediction using AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    # Allow Frontend on Port 3003
    allow_origins=["http://localhost:3003", "http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PatientData(BaseModel):
    age: int = Field(..., ge=0, le=120)
    gender: str
    chronic_conditions: List[str] = []
    recent_admissions: int = Field(default=0, ge=0)
    vital_signs: Optional[str] = None

class PredictionResponse(BaseModel):
    risk_level: str
    confidence: float
    probability_distribution: Dict[str, float]
    timestamp: datetime

class AnalysisRequest(BaseModel):
    patient_data: PatientData
    prediction: str
    confidence: float

class AnalysisResponse(BaseModel):
    analysis: str

class AIModel:
    def __init__(self):
        self.name = "Risk Stratification Model"
        self.classes = ['Low Risk', 'Moderate Risk', 'High Risk']
        logger.info(f"{self.name} initialized")
    
    async def predict(self, patient: PatientData) -> Dict:
        await asyncio.sleep(0.1) # Simulate inference
        
        # Rule-based Mock Logic (Simulating a trained model)
        # Risk Score Calculation
        score = 0
        score += (patient.age / 100.0) * 0.3
        score += (len(patient.chronic_conditions) * 0.2)
        score += (patient.recent_admissions * 0.25)
        
        # Normalize score 0-1 (roughly)
        score = min(score, 0.99)
        
        # Determine Class
        if score < 0.3:
            prediction = "Low Risk"
            probs = {"Low Risk": 0.8, "Moderate Risk": 0.15, "High Risk": 0.05}
        elif score < 0.6:
            prediction = "Moderate Risk"
            probs = {"Low Risk": 0.2, "Moderate Risk": 0.7, "High Risk": 0.1}
        else:
            prediction = "High Risk"
            probs = {"Low Risk": 0.05, "Moderate Risk": 0.15, "High Risk": 0.8}
            
        return {
            "prediction": prediction,
            "confidence": probs[prediction], 
            "probabilities": probs
        }

model = AIModel()

@app.get("/")
async def root():
    return {"message": "Patient Risk Stratification API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/api/v1/predict", response_model=PredictionResponse)
async def predict_risk(data: PatientData):
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
        # Construct Context string
        patient = request.patient_data
        context_str = f"Age: {patient.age}, Gender: {patient.gender}, Conditions: {', '.join(patient.chronic_conditions)}, Recent Admissions: {patient.recent_admissions}"
        
        analysis = llm_assistant.analyze_risk({
            "patient_context": context_str,
            "features": "Simulated latent vectors derived from patient history",
            "prediction": request.prediction,
            "confidence": request.confidence
        })
        return AnalysisResponse(analysis=analysis)
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
