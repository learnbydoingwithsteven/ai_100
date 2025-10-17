"""
FastAPI Backend - Complete Example
Medical Image Diagnosis Application
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import numpy as np
import logging
from datetime import datetime
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Medical Image Diagnosis API",
    description="AI-powered medical image analysis system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://app.example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str

class PredictionRequest(BaseModel):
    data: List[float] = Field(..., description="Input features for prediction")
    model_type: str = Field(default="cnn", description="Model type to use")
    confidence_threshold: float = Field(default=0.5, ge=0.0, le=1.0)

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    probabilities: Dict[str, float]
    processing_time: float
    model_version: str
    timestamp: datetime

class TrainingRequest(BaseModel):
    epochs: int = Field(default=10, ge=1, le=100)
    batch_size: int = Field(default=32, ge=1, le=256)
    learning_rate: float = Field(default=0.001, ge=0.0001, le=0.1)

class TrainingResponse(BaseModel):
    status: str
    task_id: str
    message: str

class MetricsResponse(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    confusion_matrix: List[List[int]]
    training_time: float
    last_updated: datetime

# Mock ML Model (replace with actual model)
class MLModel:
    def __init__(self):
        self.classes = ['Normal', 'Abnormal', 'Critical']
        self.version = "1.0.0"
    
    async def predict(self, data: List[float]) -> Dict:
        """Async prediction"""
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        # Mock prediction
        probabilities = {
            'Normal': 0.7,
            'Abnormal': 0.2,
            'Critical': 0.1
        }
        prediction = max(probabilities, key=probabilities.get)
        confidence = probabilities[prediction]
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'probabilities': probabilities
        }
    
    async def train(self, epochs: int, batch_size: int, learning_rate: float):
        """Async training"""
        logger.info(f"Starting training: epochs={epochs}, batch_size={batch_size}, lr={learning_rate}")
        
        # Simulate training
        for epoch in range(epochs):
            await asyncio.sleep(0.5)
            logger.info(f"Epoch {epoch+1}/{epochs} completed")
        
        return {"status": "completed", "final_accuracy": 0.95}
    
    def get_metrics(self) -> Dict:
        """Get model metrics"""
        return {
            'accuracy': 0.95,
            'precision': 0.93,
            'recall': 0.94,
            'f1_score': 0.935,
            'confusion_matrix': [[85, 10, 5], [8, 82, 10], [5, 8, 87]],
            'training_time': 120.5,
            'last_updated': datetime.now()
        }

# Initialize model
model = MLModel()

# Background task storage (use Redis/Celery in production)
training_tasks = {}

# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Medical Image Diagnosis API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )

@app.post("/api/v1/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(request: PredictionRequest):
    """
    Make a prediction on input data
    
    - **data**: List of input features
    - **model_type**: Type of model to use (cnn, resnet, efficientnet)
    - **confidence_threshold**: Minimum confidence threshold
    """
    try:
        start_time = datetime.now()
        
        # Validate input
        if len(request.data) == 0:
            raise HTTPException(status_code=400, detail="Input data cannot be empty")
        
        # Make prediction
        result = await model.predict(request.data)
        
        # Check confidence threshold
        if result['confidence'] < request.confidence_threshold:
            logger.warning(f"Low confidence prediction: {result['confidence']}")
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return PredictionResponse(
            prediction=result['prediction'],
            confidence=result['confidence'],
            probabilities=result['probabilities'],
            processing_time=processing_time,
            model_version=model.version,
            timestamp=datetime.now()
        )
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/api/v1/predict/batch", tags=["Prediction"])
async def predict_batch(requests: List[PredictionRequest]):
    """Batch prediction endpoint"""
    results = []
    for req in requests:
        result = await predict(req)
        results.append(result)
    return {"predictions": results, "count": len(results)}

@app.post("/api/v1/train", response_model=TrainingResponse, tags=["Training"])
async def train_model(request: TrainingRequest, background_tasks: BackgroundTasks):
    """
    Train or retrain the model
    
    - **epochs**: Number of training epochs
    - **batch_size**: Batch size for training
    - **learning_rate**: Learning rate
    """
    try:
        # Generate task ID
        task_id = f"train_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Add training to background tasks
        background_tasks.add_task(
            model.train,
            request.epochs,
            request.batch_size,
            request.learning_rate
        )
        
        # Store task info
        training_tasks[task_id] = {
            'status': 'running',
            'started_at': datetime.now(),
            'parameters': request.dict()
        }
        
        return TrainingResponse(
            status="started",
            task_id=task_id,
            message=f"Training started with {request.epochs} epochs"
        )
    
    except Exception as e:
        logger.error(f"Training error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@app.get("/api/v1/training/{task_id}", tags=["Training"])
async def get_training_status(task_id: str):
    """Get training task status"""
    if task_id not in training_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return training_tasks[task_id]

@app.get("/api/v1/metrics", response_model=MetricsResponse, tags=["Metrics"])
async def get_metrics():
    """Get model performance metrics"""
    try:
        metrics = model.get_metrics()
        return MetricsResponse(**metrics)
    except Exception as e:
        logger.error(f"Metrics error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")

@app.post("/api/v1/upload", tags=["Upload"])
async def upload_file(file: UploadFile = File(...)):
    """
    Upload medical image for analysis
    
    - **file**: Medical image file (DICOM, PNG, JPG)
    """
    try:
        # Validate file type
        allowed_types = ['image/png', 'image/jpeg', 'application/dicom']
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {allowed_types}"
            )
        
        # Read file
        contents = await file.read()
        
        # Process file (mock)
        logger.info(f"Received file: {file.filename}, size: {len(contents)} bytes")
        
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(contents),
            "status": "uploaded"
        }
    
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/api/v1/models", tags=["Models"])
async def list_models():
    """List available models"""
    return {
        "models": [
            {
                "id": "cnn_v1",
                "name": "CNN Model v1.0",
                "type": "cnn",
                "accuracy": 0.95,
                "status": "active"
            },
            {
                "id": "resnet_v1",
                "name": "ResNet Model v1.0",
                "type": "resnet",
                "accuracy": 0.97,
                "status": "active"
            }
        ]
    }

@app.get("/api/v1/models/{model_id}", tags=["Models"])
async def get_model_details(model_id: str):
    """Get model details"""
    return {
        "id": model_id,
        "name": f"Model {model_id}",
        "version": "1.0.0",
        "accuracy": 0.95,
        "created_at": datetime.now(),
        "parameters": {
            "layers": 50,
            "input_size": [224, 224, 3],
            "output_classes": 3
        }
    }

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "timestamp": datetime.now().isoformat()
        }
    )

# Startup/Shutdown events
@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")
    # Initialize database connections, load models, etc.

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down...")
    # Close database connections, cleanup, etc.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
