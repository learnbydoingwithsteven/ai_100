# 🏥 Patient Risk Stratification AI

## Overview
AI-powered predictive model for hospital readmission risk assessment. Combines quantitative ML models with qualitative GenAI analysis.

## 🏗️ Architecture
- **Frontend**: React 18 + Vite (Port 3003)
- **Backend**: FastAPI + Python (Port 8003)
- **AI Engine**: Random Forest (Legacy Mock) + Ollama (qwen2.5) for Clinical Reporting.

## 🚀 Quick Start

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev -- --port 3003
```

## 📊 Features
- **Patient Profile Form**: Age, Gender, Conditions, History.
- **Risk Assessment**: Low/Moderate/High risk classification.
- **Interactive Visualizations**: Risk probability distribution.
- **AI Consultant**: "Generate Clinical Report" explains the risk factors in plain English.

## 📸 Screenshots
*(Coming soon via automated testing)*
