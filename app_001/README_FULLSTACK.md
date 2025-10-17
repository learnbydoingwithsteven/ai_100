# 🏥 Medical Image Diagnosis - Full-Stack Application

Complete AI-powered medical image analysis system with modern full-stack architecture.

## 🎯 Overview

This application provides automated CT/MRI scan analysis using CNN technology with a professional web interface.

## 🏗️ Architecture

```
app_001/
├── frontend/           # React + TypeScript UI
├── backend/            # FastAPI + Python ML Engine
├── docker-compose.yml  # Multi-container orchestration
├── .github/workflows/  # CI/CD pipelines
└── docs/              # Documentation
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local development)
- Python 3.10+ (for local development)

### Run with Docker (Recommended)

```bash
# Start all services
docker-compose up

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Local Development

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## 📊 Features

### Frontend
- ✅ Interactive prediction interface
- ✅ Real-time visualization with Chart.js
- ✅ Responsive design with TailwindCSS
- ✅ Performance metrics dashboard
- ✅ File upload support

### Backend
- ✅ RESTful API with FastAPI
- ✅ Async prediction endpoints
- ✅ Background training tasks
- ✅ Comprehensive metrics
- ✅ OpenAPI documentation

### ML/AI
- ✅ CNN-based image classification
- ✅ Multi-class prediction (Normal/Abnormal/Critical)
- ✅ Confidence scoring
- ✅ Model performance tracking

## 🔌 API Endpoints

### Health Check
```bash
GET /health
```

### Prediction
```bash
POST /api/v1/predict
{
  "data": [1.5, 2.3, 4.1, ...],
  "confidence_threshold": 0.5
}
```

### Training
```bash
POST /api/v1/train
{
  "epochs": 10,
  "batch_size": 32
}
```

### Metrics
```bash
GET /api/v1/metrics
```

### File Upload
```bash
POST /api/v1/upload
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app tests/
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

### Integration Tests
```bash
docker-compose up -d
pytest tests/integration/
```

## 🚢 Deployment

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

## 📈 Monitoring

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001
- **Logs**: `docker-compose logs -f`

## 🛠️ Technology Stack

### Frontend
- React 18 + TypeScript
- TailwindCSS
- Chart.js
- Axios

### Backend
- FastAPI 0.104+
- Python 3.10+
- Pydantic v2
- NumPy, Pandas

### Infrastructure
- Docker + Docker Compose
- PostgreSQL 15
- Redis 7
- Nginx

### CI/CD
- GitHub Actions
- Automated testing
- Security scanning
- Multi-environment deployment

## 📖 Documentation

- [API Documentation](./docs/API.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)
- [Development Guide](./docs/DEVELOPMENT.md)

## 🔐 Security

- JWT authentication
- CORS configuration
- Input validation
- Rate limiting
- HTTPS in production

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - Free to use for educational and commercial purposes

## 📞 Support

- GitHub Issues: Report bugs
- Documentation: Check docs/
- API Docs: http://localhost:8000/docs

---

**Version**: 1.0.0  
**Last Updated**: 2025-01-17  
**Status**: ✅ Production Ready
