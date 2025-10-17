# 🚀 Full-Stack Migration Guide

## Overview

This guide explains how to migrate all 100 AI applications from monolithic Python scripts to a modern **full-stack architecture** with proper front-end/back-end separation and comprehensive CI/CD pipelines.

## Architecture Transformation

### Before (Monolithic)
```
app_XXX/
├── app.py              # All logic in one file
├── requirements.txt
└── README.md
```

### After (Full-Stack)
```
app_XXX/
├── frontend/           # React + TypeScript
├── backend/            # FastAPI + Python
├── docker-compose.yml  # Orchestration
├── .github/workflows/  # CI/CD pipelines
└── docs/               # Documentation
```

## Migration Process

### Step 1: Run Migration Script

```bash
cd ai_100
python migrate_to_fullstack.py
```

This will:
- ✅ Create frontend structure (React + TypeScript)
- ✅ Create backend structure (FastAPI + Python)
- ✅ Generate Docker configurations
- ✅ Setup CI/CD pipelines (GitHub Actions)
- ✅ Create comprehensive documentation

### Step 2: Manual Code Migration

For each application, you'll need to:

#### Backend Migration

1. **Extract ML Logic** from `app.py`:
```python
# Old: app.py (monolithic)
class MedicalImageDiagnosisAI:
    def train_model(self, X_train, y_train):
        # Training logic
        pass

# New: backend/app/ml/model.py (separated)
class MLModel:
    def train(self, X_train, y_train):
        # Training logic
        pass
```

2. **Create API Endpoints** in `backend/app/api/endpoints/`:
```python
# backend/app/api/endpoints/predict.py
from fastapi import APIRouter, UploadFile
from app.ml.model import MLModel

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile):
    model = MLModel()
    result = await model.predict(file)
    return {"predictions": result}
```

3. **Add Data Models** in `backend/app/models/`:
```python
# backend/app/models/schemas.py
from pydantic import BaseModel

class PredictionRequest(BaseModel):
    data: list[float]
    parameters: dict

class PredictionResponse(BaseModel):
    predictions: list[float]
    confidence: float
    processing_time: float
```

#### Frontend Migration

1. **Create API Service** in `frontend/src/services/`:
```typescript
// frontend/src/services/api.ts
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const predict = async (data: any) => {
  const response = await axios.post(`${API_URL}/api/v1/predict`, data);
  return response.data;
};
```

2. **Create UI Components** in `frontend/src/components/`:
```typescript
// frontend/src/components/PredictionForm.tsx
import React, { useState } from 'react';
import { predict } from '../services/api';

export const PredictionForm: React.FC = () => {
  const [result, setResult] = useState(null);
  
  const handleSubmit = async (data: any) => {
    const prediction = await predict(data);
    setResult(prediction);
  };
  
  return (
    <div>
      {/* Form UI */}
    </div>
  );
};
```

3. **Create Visualization Components**:
```typescript
// frontend/src/components/ResultsChart.tsx
import { Chart } from 'react-chartjs-2';

export const ResultsChart: React.FC<{data: any}> = ({data}) => {
  return <Chart type="bar" data={data} />;
};
```

### Step 3: Configure Environment Variables

Create `.env` file in each app directory:

```bash
# Backend
DATABASE_URL=postgresql://user:password@localhost:5432/aiapp
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
DEBUG=True

# Frontend
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENV=development
```

### Step 4: Test Locally

```bash
# Start all services
docker-compose up -d

# Check backend health
curl http://localhost:8000/health

# Check frontend
open http://localhost:3000

# Run tests
cd backend && pytest
cd frontend && npm test
```

### Step 5: Setup CI/CD

1. **Create GitHub Repository** for each app
2. **Add Secrets** to GitHub:
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `SNYK_TOKEN`
   - `SONAR_TOKEN`

3. **Push Code**:
```bash
git init
git add .
git commit -m "Migrate to full-stack architecture"
git remote add origin <repo-url>
git push -u origin main
```

4. **CI/CD will automatically**:
   - Run tests on every push
   - Build Docker images
   - Deploy to staging on merge to main
   - Deploy to production on tag creation

## Application-Specific Migration Examples

### Example 1: Medical Image Diagnosis (App 001)

**Backend Structure:**
```
backend/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       ├── predict.py      # Image prediction endpoint
│   │       ├── train.py        # Model training endpoint
│   │       └── metrics.py      # Performance metrics
│   ├── ml/
│   │   ├── model.py            # CNN model definition
│   │   ├── preprocessing.py    # Image preprocessing
│   │   └── inference.py        # Inference logic
│   └── main.py
```

**Frontend Structure:**
```
frontend/
├── src/
│   ├── components/
│   │   ├── ImageUploader.tsx   # Drag-drop image upload
│   │   ├── PredictionResult.tsx # Show diagnosis
│   │   └── ConfusionMatrix.tsx  # Visualization
│   ├── pages/
│   │   ├── Dashboard.tsx       # Main dashboard
│   │   └── Training.tsx        # Model training UI
│   └── services/
│       └── medicalApi.ts       # API calls
```

### Example 2: Stock Price Predictor (App 021)

**Backend Structure:**
```
backend/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       ├── forecast.py     # Time series forecasting
│   │       └── historical.py   # Historical data
│   ├── ml/
│   │   ├── lstm_model.py       # LSTM model
│   │   └── features.py         # Feature engineering
│   └── main.py
```

**Frontend Structure:**
```
frontend/
├── src/
│   ├── components/
│   │   ├── StockChart.tsx      # Interactive chart
│   │   ├── ForecastPanel.tsx   # Prediction display
│   │   └── MetricsCard.tsx     # Performance metrics
│   └── services/
│       └── stockApi.ts
```

## Best Practices

### Backend

1. **Async/Await**: Use async functions for I/O operations
```python
@router.post("/predict")
async def predict(request: PredictionRequest):
    result = await model.predict_async(request.data)
    return result
```

2. **Error Handling**: Implement comprehensive error handling
```python
from fastapi import HTTPException

@router.post("/predict")
async def predict(request: PredictionRequest):
    try:
        result = await model.predict(request.data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

3. **Caching**: Use Redis for frequent queries
```python
from app.core.cache import cache

@router.get("/models/{model_id}")
@cache(expire=3600)
async def get_model(model_id: str):
    return await db.get_model(model_id)
```

4. **Background Tasks**: Use Celery for long-running tasks
```python
from app.celery_app import celery_app

@celery_app.task
def train_model_task(data):
    model.train(data)
    return "Training complete"
```

### Frontend

1. **State Management**: Use Redux or Zustand
```typescript
// store/predictionSlice.ts
import { createSlice } from '@reduxjs/toolkit';

export const predictionSlice = createSlice({
  name: 'prediction',
  initialState: { result: null, loading: false },
  reducers: {
    setResult: (state, action) => {
      state.result = action.payload;
    }
  }
});
```

2. **Error Boundaries**: Catch React errors
```typescript
class ErrorBoundary extends React.Component {
  componentDidCatch(error, errorInfo) {
    console.error('Error:', error, errorInfo);
  }
  render() {
    return this.props.children;
  }
}
```

3. **Code Splitting**: Lazy load components
```typescript
const Dashboard = React.lazy(() => import('./pages/Dashboard'));

<Suspense fallback={<Loading />}>
  <Dashboard />
</Suspense>
```

## Deployment

### Development
```bash
docker-compose up
```

### Staging
```bash
docker-compose -f docker-compose.staging.yml up -d
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes (Advanced)
```bash
kubectl apply -f k8s/
```

## Monitoring

### Application Metrics
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001

### Logs
```bash
# Backend logs
docker-compose logs -f backend

# Frontend logs
docker-compose logs -f frontend

# All logs
docker-compose logs -f
```

### Health Checks
```bash
# Backend
curl http://localhost:8000/health

# Database
docker-compose exec postgres pg_isready

# Redis
docker-compose exec redis redis-cli ping
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
```bash
# Find process using port
lsof -i :8000
# Kill process
kill -9 <PID>
```

2. **Database Connection Failed**
```bash
# Check database status
docker-compose ps postgres
# Restart database
docker-compose restart postgres
```

3. **Frontend Build Fails**
```bash
# Clear cache
cd frontend
rm -rf node_modules package-lock.json
npm install
```

4. **Backend Import Errors**
```bash
# Rebuild backend
docker-compose build backend
docker-compose up -d backend
```

## Migration Checklist

- [ ] Run migration script
- [ ] Extract ML logic to backend/app/ml/
- [ ] Create API endpoints in backend/app/api/
- [ ] Create Pydantic models in backend/app/models/
- [ ] Build React components in frontend/src/components/
- [ ] Create API service layer in frontend/src/services/
- [ ] Configure environment variables (.env)
- [ ] Test locally with docker-compose
- [ ] Setup GitHub repository
- [ ] Configure GitHub Actions secrets
- [ ] Push code and verify CI/CD
- [ ] Deploy to staging
- [ ] Run smoke tests
- [ ] Deploy to production

## Support

For issues or questions:
1. Check [ARCHITECTURE.md](./ARCHITECTURE.md)
2. Review application-specific docs in `docs/`
3. Check GitHub Actions logs for CI/CD issues
4. Review Docker logs for runtime issues

---

**Migration Version**: 2.0  
**Last Updated**: 2025-01-17  
**Estimated Time per App**: 2-4 hours
