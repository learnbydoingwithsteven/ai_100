# 🚀 Running All 100 Applications

## Quick Reference Guide

### Run Single Application

```bash
cd app_001
docker-compose up
```

Access at:
- Frontend: http://localhost:3001
- Backend: http://localhost:8001
- API Docs: http://localhost:8001/docs

### Run Multiple Applications

Each app uses unique ports, so you can run them all simultaneously:

```bash
# Terminal 1
cd app_001 && docker-compose up

# Terminal 2  
cd app_002 && docker-compose up

# Terminal 3
cd app_003 && docker-compose up
```

## Port Reference Table

| App # | Frontend | Backend | PostgreSQL | Redis | App Name |
|-------|----------|---------|------------|-------|----------|
| 001 | 3001 | 8001 | 5433 | 6380 | Medical Image Diagnosis |
| 002 | 3002 | 8002 | 5434 | 6381 | Drug Discovery Predictor |
| 003 | 3003 | 8003 | 5435 | 6382 | Patient Risk Stratification |
| 004 | 3004 | 8004 | 5436 | 6383 | ECG Anomaly Detection |
| 005 | 3005 | 8005 | 5437 | 6384 | Skin Lesion Classifier |
| ... | ... | ... | ... | ... | ... |
| 100 | 3100 | 8100 | 5532 | 6479 | AI Ethics Auditor |

## Batch Operations

### Start All Healthcare Apps (1-20)

```bash
for i in {1..20}; do
  cd app_$(printf "%03d" $i)
  docker-compose up -d
  cd ..
done
```

### Start All Finance Apps (21-40)

```bash
for i in {21..40}; do
  cd app_$(printf "%03d" $i)
  docker-compose up -d
  cd ..
done
```

### Start All Computer Vision Apps (41-60)

```bash
for i in {41..60}; do
  cd app_$(printf "%03d" $i)
  docker-compose up -d
  cd ..
done
```

### Start All NLP Apps (61-80)

```bash
for i in {61..80}; do
  cd app_$(printf "%03d" $i)
  docker-compose up -d
  cd ..
done
```

### Start All Specialized AI Apps (81-100)

```bash
for i in {81..100}; do
  cd app_$(printf "%03d" $i)
  docker-compose up -d
  cd ..
done
```

### Start ALL 100 Apps

```bash
for i in {1..100}; do
  cd app_$(printf "%03d" $i)
  docker-compose up -d
  cd ..
  echo "Started app_$(printf "%03d" $i)"
done
```

## Stop Operations

### Stop Single App

```bash
cd app_001
docker-compose down
```

### Stop All Apps

```bash
for i in {1..100}; do
  cd app_$(printf "%03d" $i)
  docker-compose down
  cd ..
done
```

### Stop and Remove Volumes

```bash
for i in {1..100}; do
  cd app_$(printf "%03d" $i)
  docker-compose down -v
  cd ..
done
```

## Health Checks

### Check Single App

```bash
# Backend health
curl http://localhost:8001/health

# Frontend (should return HTML)
curl http://localhost:3001
```

### Check All Apps

```bash
for i in {1..100}; do
  port=$((8000 + i))
  echo "Checking app_$(printf "%03d" $i) on port $port"
  curl -s http://localhost:$port/health | jq
done
```

## Monitoring

### View Logs for Single App

```bash
cd app_001
docker-compose logs -f
```

### View Backend Logs Only

```bash
cd app_001
docker-compose logs -f backend
```

### View All App Statuses

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

## Testing

### Test Single App

```bash
cd app_001/backend
pytest -v
```

### Test All Apps

```bash
for i in {1..100}; do
  echo "Testing app_$(printf "%03d" $i)"
  cd app_$(printf "%03d" $i)/backend
  pytest
  cd ../..
done
```

## Resource Management

### Check Docker Resource Usage

```bash
docker stats
```

### Clean Up Unused Resources

```bash
# Remove stopped containers
docker container prune -f

# Remove unused images
docker image prune -a -f

# Remove unused volumes
docker volume prune -f

# Remove unused networks
docker network prune -f
```

## Development Workflow

### Rebuild Single App

```bash
cd app_001
docker-compose build
docker-compose up
```

### Rebuild All Apps

```bash
for i in {1..100}; do
  cd app_$(printf "%03d" $i)
  docker-compose build
  cd ..
done
```

## Production Deployment

### Deploy Single App to Production

```bash
cd app_001
docker-compose -f docker-compose.prod.yml up -d
```

### Deploy All Apps to Production

```bash
for i in {1..100}; do
  cd app_$(printf "%03d" $i)
  docker-compose -f docker-compose.prod.yml up -d
  cd ..
done
```

## Troubleshooting

### Port Already in Use

```bash
# Find what's using the port
lsof -i :8001

# Kill the process
kill -9 <PID>
```

### Container Won't Start

```bash
# Check logs
docker-compose logs backend

# Rebuild container
docker-compose build backend
docker-compose up backend
```

### Database Connection Issues

```bash
# Restart database
docker-compose restart postgres

# Check database logs
docker-compose logs postgres
```

## Performance Tips

### Run Apps in Background

```bash
docker-compose up -d
```

### Limit Resource Usage

Edit `docker-compose.yml`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

### Use Docker Compose Profiles

```yaml
services:
  backend:
    profiles: ["dev", "prod"]
```

Run with:
```bash
docker-compose --profile dev up
```

## Useful Commands

### View All Running Apps

```bash
docker ps --filter "name=app_" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Stop All Running Containers

```bash
docker stop $(docker ps -q)
```

### Remove All Containers

```bash
docker rm $(docker ps -a -q)
```

### View Disk Usage

```bash
docker system df
```

### Complete Cleanup

```bash
docker system prune -a --volumes -f
```

## Access URLs Quick Reference

### Healthcare Apps (1-20)
- App 001: http://localhost:3001 (Medical Image Diagnosis)
- App 002: http://localhost:3002 (Drug Discovery)
- App 003: http://localhost:3003 (Patient Risk)
- ...

### Finance Apps (21-40)
- App 021: http://localhost:3021 (Stock Predictor)
- App 022: http://localhost:3022 (Credit Risk)
- App 023: http://localhost:3023 (Fraud Detection)
- ...

### Computer Vision Apps (41-60)
- App 041: http://localhost:3041 (Object Detection)
- App 042: http://localhost:3042 (Facial Recognition)
- App 043: http://localhost:3043 (Style Transfer)
- ...

### NLP Apps (61-80)
- App 061: http://localhost:3061 (Sentiment Analysis)
- App 062: http://localhost:3062 (Text Summarizer)
- App 063: http://localhost:3063 (Translation)
- ...

### Specialized AI Apps (81-100)
- App 081: http://localhost:3081 (Predictive Maintenance)
- App 082: http://localhost:3082 (Energy Optimizer)
- App 100: http://localhost:3100 (AI Ethics Auditor)
- ...

---

**Pro Tip**: Use tmux or screen to manage multiple terminal sessions when running many apps simultaneously.

**System Requirements**: 
- For running all 100 apps: 32GB+ RAM recommended
- For running 10 apps: 8GB RAM sufficient
- For running 1 app: 2GB RAM sufficient
