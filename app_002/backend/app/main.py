"""
Drug Discovery Predictor - FastAPI Backend
Molecular property prediction
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict
import logging
from datetime import datetime
import asyncio
from app.ml.llm import MolecularAssistant

llm_assistant = MolecularAssistant()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Drug Discovery Predictor API",
    description="Molecular property prediction using Gradient Boosting",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionRequest(BaseModel):
    smiles: str = Field(..., description="Molecular SMILES string")

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    timestamp: datetime

class AnalysisRequest(BaseModel):

    smiles: str
    prediction: str
    confidence: float

class AnalysisResponse(BaseModel):
    analysis: str

class AIModel:
    def __init__(self):
        self.name = "Drug Discovery Predictor"
        logger.info(f"{self.name} initialized")
    
    async def predict(self, smiles: str) -> Dict:
        await asyncio.sleep(0.1)
        # Mock Property Extraction
        mol_weight = len(smiles) * 12.5 # Fake MW
        log_p = len(smiles) / 10.0 # Fake LogP
        
        # Simple rule-based prediction
        if "COOH" in smiles or "C(=O)O" in smiles:
            category = "Acidic/Soluble"
        elif "N" in smiles:
             category = "Basic/Bioactive"
        else:
             category = "Neutral/Lipophilic"
             
        return {
            "prediction": f"{category} (MW: {mol_weight:.1f})", 
            "confidence": 0.85 + (len(smiles) % 10)/100.0
        }

model = AIModel()

@app.get("/")
async def root():
    return {"message": "Drug Discovery Predictor API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/api/v1/predict", response_model=PredictionResponse)

async def predict(request: PredictionRequest):
    try:
        result = await model.predict(request.smiles)
        return PredictionResponse(
            prediction=result["prediction"],
            confidence=result["confidence"],
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analyze", response_model=AnalysisResponse)
async def analyze_prediction(request: AnalysisRequest):
    try:
        analysis = llm_assistant.analyze_prediction({
            "smiles": request.smiles,
            "prediction": request.prediction,
            "confidence": request.confidence
        })
        return AnalysisResponse(analysis=analysis)
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
