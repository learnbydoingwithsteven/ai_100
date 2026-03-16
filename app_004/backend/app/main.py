"""
Diabetes Progression - FastAPI Backend
Early onset prediction
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import logging
from datetime import datetime
import asyncio
from app.ml.llm import DiabetesSpecialist

# Initialize LLM
llm_specialist = DiabetesSpecialist()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Diabetes Progression AI API",
    description="Predicts risk of diabetes progression based on clinical markers",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    # Allow Frontend on Port 3004
    allow_origins=["http://localhost:3004", "http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PatientVitals(BaseModel):
    glucose_fasting: float = Field(..., ge=0, le=500)
    hba1c: float = Field(..., ge=0, le=20)
    bmi: float = Field(..., ge=0, le=100)
    age: int = Field(..., ge=0, le=120)
    hypertension: bool = False

class PredictionResponse(BaseModel):
    risk_level: str
    confidence: float
    probability_distribution: Dict[str, float]
    timestamp: datetime

class AnalysisRequest(BaseModel):
    patient_data: PatientVitals
    prediction: str
    confidence: float

class AnalysisResponse(BaseModel):
    analysis: str

class AIModel:
    def __init__(self):
        self.name = "Diabetes Progression Model"
        self.classes = ['Low Risk', 'Moderate Risk', 'High Risk']
        logger.info(f"{self.name} initialized")
    
    async def predict(self, patient: PatientVitals) -> Dict:
        await asyncio.sleep(0.1) 
        
        # Rule-based Mock Logic
        score = 0
        
        # Glucose Factor (Normal < 100, Prediabetes 100-125, Diabetes > 126)
        if patient.glucose_fasting > 126: score += 0.4
        elif patient.glucose_fasting > 100: score += 0.2
        
        # HbA1c Factor (Normal < 5.7, Prediabetes 5.7-6.4, Diabetes > 6.5)
        if patient.hba1c > 6.5: score += 0.4
        elif patient.hba1c > 5.7: score += 0.2
        
        # BMI Factor
        if patient.bmi > 30: score += 0.1
        
        # Age Factor
        if patient.age > 45: score += 0.1

        score = min(score, 0.99)
        
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
    return {"message": "Diabetes Progression API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/api/v1/predict", response_model=PredictionResponse)
async def predict_risk(data: PatientVitals):
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
        patient = request.patient_data
        context_str = f"Glucose (Fasting): {patient.glucose_fasting} mg/dL, HbA1c: {patient.hba1c}%, BMI: {patient.bmi}, Age: {patient.age}, Hypertension: {patient.hypertension}"
        
        analysis = llm_specialist.analyze_progression({
            "patient_context": context_str,
            "prediction": request.prediction,
            "confidence": request.confidence
        })
        return AnalysisResponse(analysis=analysis)
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
