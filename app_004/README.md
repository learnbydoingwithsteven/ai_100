# 🩸 Diabetes Progression AI

## Overview
AI model for predicting early onset of diabetes based on clinical biomarkers (Glucose, HbA1c, BMI). Includes an Endocrinologist AI Agent for personalized management advice.

## 🏗️ Architecture
- **Frontend**: React 18 + Vite (Port 3004)
- **Backend**: FastAPI + Python (Port 8004)
- **AI Engine**: Rule-based Risk Model + Diabetes Specialist LLM Persona.

## 🚀 Quick Start

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev -- --port 3004
```

## 📊 Features
- **Biomarker Analysis**: Fasting Glucose, HbA1c, BMI.
- **Risk Stratification**: Low/Moderate/High progression risk.
- **Endocrinologist Report**: LLM-generated lifestyle and medical recommendations.
- **Visuals**: Risk probability charts.

## 📸 Screenshots
*(Coming soon via automated testing)*
