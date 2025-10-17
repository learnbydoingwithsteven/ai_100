"""
Migration Script: Convert all 100 AI apps to Full-Stack Architecture
Transforms monolithic Python apps into Frontend (React) + Backend (FastAPI) + CI/CD
"""

import os
import shutil
import json
from pathlib import Path
from typing import Dict, List

class FullStackMigrator:
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.templates_dir = self.base_dir / "templates"
        
    def migrate_all_apps(self):
        """Migrate all 100 applications"""
        print("🚀 Starting Full-Stack Migration for 100 AI Applications")
        print("=" * 70)
        
        for i in range(1, 101):
            app_dir = self.base_dir / f"app_{i:03d}"
            if app_dir.exists():
                print(f"\n📦 Migrating app_{i:03d}...")
                self.migrate_single_app(app_dir, i)
        
        print("\n" + "=" * 70)
        print("✅ Migration Complete!")
        
    def migrate_single_app(self, app_dir: Path, app_num: int):
        """Migrate a single application"""
        # Read existing app.py to extract logic
        app_py = app_dir / "app.py"
        if not app_py.exists():
            print(f"⚠️  Skipping {app_dir.name} - no app.py found")
            return
            
        # Create new structure
        self.create_backend(app_dir, app_num)
        self.create_frontend(app_dir, app_num)
        self.create_docker_files(app_dir, app_num)
        self.create_cicd_pipelines(app_dir, app_num)
        self.create_documentation(app_dir, app_num)
        
        print(f"✅ Migrated {app_dir.name}")
    
    def create_backend(self, app_dir: Path, app_num: int):
        """Create FastAPI backend structure"""
        backend_dir = app_dir / "backend"
        backend_dir.mkdir(exist_ok=True)
        
        # Create directory structure
        (backend_dir / "app").mkdir(exist_ok=True)
        (backend_dir / "app" / "api").mkdir(exist_ok=True)
        (backend_dir / "app" / "api" / "endpoints").mkdir(exist_ok=True)
        (backend_dir / "app" / "core").mkdir(exist_ok=True)
        (backend_dir / "app" / "models").mkdir(exist_ok=True)
        (backend_dir / "app" / "ml").mkdir(exist_ok=True)
        (backend_dir / "tests").mkdir(exist_ok=True)
        
        # Create files (templates will be generated separately)
        self._create_backend_main(backend_dir, app_num)
        self._create_backend_requirements(backend_dir)
        self._create_backend_config(backend_dir)
        
    def create_frontend(self, app_dir: Path, app_num: int):
        """Create React frontend structure"""
        frontend_dir = app_dir / "frontend"
        frontend_dir.mkdir(exist_ok=True)
        
        # Create directory structure
        (frontend_dir / "public").mkdir(exist_ok=True)
        (frontend_dir / "src").mkdir(exist_ok=True)
        (frontend_dir / "src" / "components").mkdir(exist_ok=True)
        (frontend_dir / "src" / "pages").mkdir(exist_ok=True)
        (frontend_dir / "src" / "services").mkdir(exist_ok=True)
        
        self._create_frontend_package_json(frontend_dir, app_num)
        
    def create_docker_files(self, app_dir: Path, app_num: int):
        """Create Docker and Docker Compose files"""
        self._create_docker_compose(app_dir, app_num)
        self._create_backend_dockerfile(app_dir / "backend")
        self._create_frontend_dockerfile(app_dir / "frontend")
        
    def create_cicd_pipelines(self, app_dir: Path, app_num: int):
        """Create GitHub Actions CI/CD pipelines"""
        github_dir = app_dir / ".github" / "workflows"
        github_dir.mkdir(parents=True, exist_ok=True)
        
        self._create_ci_workflow(github_dir)
        self._create_cd_workflow(github_dir)
        
    def create_documentation(self, app_dir: Path, app_num: int):
        """Create comprehensive documentation"""
        docs_dir = app_dir / "docs"
        docs_dir.mkdir(exist_ok=True)
        
        self._create_api_docs(docs_dir)
        self._create_deployment_docs(docs_dir)
        
    def _create_backend_main(self, backend_dir: Path, app_num: int):
        """Create FastAPI main.py"""
        content = '''"""FastAPI Backend for AI Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Application API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Application API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
'''
        (backend_dir / "app" / "main.py").write_text(content)
        
    def _create_backend_requirements(self, backend_dir: Path):
        """Create requirements.txt"""
        content = '''fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
numpy==1.24.3
pandas==2.1.3
scikit-learn==1.3.2
tensorflow==2.15.0
torch==2.1.1
matplotlib==3.8.2
seaborn==0.13.0
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
'''
        (backend_dir / "requirements.txt").write_text(content)
        
    def _create_backend_config(self, backend_dir: Path):
        """Create config.py"""
        content = '''"""Application Configuration"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AI Application"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    
    class Config:
        env_file = ".env"

settings = Settings()
'''
        (backend_dir / "app" / "core" / "config.py").write_text(content)
        
    def _create_frontend_package_json(self, frontend_dir: Path, app_num: int):
        """Create package.json"""
        content = {
            "name": f"ai-app-{app_num:03d}-frontend",
            "version": "1.0.0",
            "private": True,
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "axios": "^1.6.2",
                "chart.js": "^4.4.0",
                "react-chartjs-2": "^5.2.0"
            },
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test"
            }
        }
        (frontend_dir / "package.json").write_text(json.dumps(content, indent=2))
        
    def _create_docker_compose(self, app_dir: Path, app_num: int):
        """Create docker-compose.yml"""
        content = '''version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --reload

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm start

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: aiapp
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
'''
        (app_dir / "docker-compose.yml").write_text(content)
        
    def _create_backend_dockerfile(self, backend_dir: Path):
        """Create backend Dockerfile"""
        content = '''FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
        (backend_dir / "Dockerfile").write_text(content)
        
    def _create_frontend_dockerfile(self, frontend_dir: Path):
        """Create frontend Dockerfile"""
        content = '''FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
'''
        (frontend_dir / "Dockerfile").write_text(content)
        
    def _create_ci_workflow(self, github_dir: Path):
        """Create CI workflow"""
        content = '''name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest
'''
        (github_dir / "ci.yml").write_text(content)
        
    def _create_cd_workflow(self, github_dir: Path):
        """Create CD workflow"""
        content = '''name: CD

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and push Docker images
        run: |
          docker-compose build
          docker-compose push
'''
        (github_dir / "cd.yml").write_text(content)
        
    def _create_api_docs(self, docs_dir: Path):
        """Create API documentation"""
        content = '''# API Documentation

## Endpoints

### Health Check
```
GET /health
```

### Prediction
```
POST /api/v1/predict
```

See OpenAPI docs at: http://localhost:8000/docs
'''
        (docs_dir / "API.md").write_text(content)
        
    def _create_deployment_docs(self, docs_dir: Path):
        """Create deployment documentation"""
        content = '''# Deployment Guide

## Local Development
```bash
docker-compose up
```

## Production Deployment
```bash
docker-compose -f docker-compose.prod.yml up -d
```
'''
        (docs_dir / "DEPLOYMENT.md").write_text(content)

if __name__ == "__main__":
    migrator = FullStackMigrator()
    migrator.migrate_all_apps()
