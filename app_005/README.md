# 🔬 Skin Lesion Classifier AI

## Overview
AI-powered assistant for early melanoma detection using the ABCD rule (Asymmetry, Border, Color, Diameter). Features a Dermatologist AI Agent for educational guidance.

## 🏗️ Architecture
- **Frontend**: React 18 + Vite (Port 3005)
- **Backend**: FastAPI + Python (Port 8005)
- **AI Engine**: Rule-based ABCD Heuristic + Ollama (qwen2.5) for detailed analysis.

## 🚀 Quick Start

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8005 --reload
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev -- --port 3005
```

## 📊 Features
- **ABCD Assessment**: Interactive sliders for Asymmetry, Border, Color, Diameter.
- **Risk Classification**: Benign/Suspicious/Malignant.
- **Dermatologist Report**: AI-generated interpretation of findings.
- **Visuals**: Probability distribution charts.

## 📸 Screenshots
*(Coming soon via automated testing)*
