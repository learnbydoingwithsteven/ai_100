# 🚀 Quick Reference Guide

## Essential Commands

### Migration
```bash
# Migrate all 100 apps to full-stack
python migrate_to_fullstack.py

# Migrate single app
python migrate_to_fullstack.py --app app_001
```

### Development
```bash
# Start application
cd app_001
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild containers
docker-compose build
docker-compose up
```

### Testing
```bash
# Backend tests
cd backend
pytest
pytest --cov=app tests/

# Frontend tests
cd frontend
npm test
npm run test:coverage

# Integration tests
docker-compose up -d
pytest tests/integration/
```

### Deployment
```bash
# Deploy to staging
docker-compose -f docker-compose.staging.yml up -d

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d

# Deploy to Kubernetes
kubectl apply -f k8s/

# Check deployment status
kubectl get pods
kubectl logs <pod-name>
```

## Application URLs

### Development
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

### Monitoring
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001
- MinIO Console: http://localhost:9001

### Database
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## Environment Variables

### Backend (.env)
```bash
# Application
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/aiapp
REDIS_URL=redis://localhost:6379/0

# Storage
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

# Monitoring
PROMETHEUS_ENABLED=True
```

### Frontend (.env)
```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENV=development
REACT_APP_VERSION=1.0.0
```

## Docker Commands

### Images
```bash
# Build images
docker-compose build

# Pull images
docker-compose pull

# List images
docker images

# Remove unused images
docker image prune
```

### Containers
```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Stop container
docker stop <container-id>

# Remove container
docker rm <container-id>

# Execute command in container
docker exec -it <container-id> bash
```

### Volumes
```bash
# List volumes
docker volume ls

# Remove unused volumes
docker volume prune

# Inspect volume
docker volume inspect <volume-name>
```

### Networks
```bash
# List networks
docker network ls

# Inspect network
docker network inspect <network-name>
```

## Git Workflow

### Feature Development
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push to remote
git push origin feature/new-feature

# Create pull request (GitHub)
# CI will run automatically
```

### Release
```bash
# Create release tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# CD will deploy to production automatically
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
```

### Database Connection Failed
```bash
# Check database status
docker-compose ps postgres

# Restart database
docker-compose restart postgres

# View database logs
docker-compose logs postgres
```

### Frontend Build Fails
```bash
# Clear cache
cd frontend
rm -rf node_modules package-lock.json
npm install

# Rebuild
npm run build
```

### Backend Import Errors
```bash
# Rebuild backend
docker-compose build backend

# Check Python version
docker-compose exec backend python --version

# Install dependencies
docker-compose exec backend pip install -r requirements.txt
```

## API Testing

### cURL Examples
```bash
# Health check
curl http://localhost:8000/health

# Prediction
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [1.0, 2.0, 3.0]}'

# Upload file
curl -X POST http://localhost:8000/api/v1/upload \
  -F "file=@image.png"
```

### HTTPie Examples
```bash
# Health check
http GET localhost:8000/health

# Prediction
http POST localhost:8000/api/v1/predict \
  data:='[1.0, 2.0, 3.0]'
```

## Database Operations

### PostgreSQL
```bash
# Connect to database
docker-compose exec postgres psql -U admin -d aiapp

# Run SQL query
docker-compose exec postgres psql -U admin -d aiapp \
  -c "SELECT * FROM users;"

# Backup database
docker-compose exec postgres pg_dump -U admin aiapp > backup.sql

# Restore database
docker-compose exec -T postgres psql -U admin aiapp < backup.sql
```

### Redis
```bash
# Connect to Redis
docker-compose exec redis redis-cli

# Get key
docker-compose exec redis redis-cli GET mykey

# Set key
docker-compose exec redis redis-cli SET mykey "value"

# Flush all data
docker-compose exec redis redis-cli FLUSHALL
```

## Monitoring

### Prometheus Queries
```promql
# Request rate
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m])

# Response time
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

### Grafana Dashboards
- Application Metrics: Dashboard ID 1
- System Metrics: Dashboard ID 2
- Database Metrics: Dashboard ID 3

## Performance Testing

### Load Testing with Locust
```bash
# Install locust
pip install locust

# Run load test
locust -f tests/load/locustfile.py \
  --host http://localhost:8000 \
  --users 100 \
  --spawn-rate 10
```

### Stress Testing with Apache Bench
```bash
# 1000 requests, 10 concurrent
ab -n 1000 -c 10 http://localhost:8000/health
```

## Security

### Scan for Vulnerabilities
```bash
# Scan Docker image
trivy image app-backend:latest

# Scan dependencies
snyk test

# Scan code
bandit -r backend/app/
```

### Update Dependencies
```bash
# Backend
cd backend
pip list --outdated
pip install --upgrade <package>

# Frontend
cd frontend
npm outdated
npm update
```

## CI/CD

### GitHub Actions
```bash
# View workflow runs
gh run list

# View specific run
gh run view <run-id>

# Re-run failed jobs
gh run rerun <run-id>
```

### Secrets Management
```bash
# Add secret to GitHub
gh secret set DOCKER_PASSWORD

# List secrets
gh secret list
```

## Useful Aliases

Add to your `.bashrc` or `.zshrc`:

```bash
# Docker Compose shortcuts
alias dc='docker-compose'
alias dcu='docker-compose up'
alias dcd='docker-compose down'
alias dcb='docker-compose build'
alias dcl='docker-compose logs -f'

# Application shortcuts
alias app-start='docker-compose up -d'
alias app-stop='docker-compose down'
alias app-logs='docker-compose logs -f'
alias app-test='docker-compose exec backend pytest'

# Git shortcuts
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
```

## Resources

### Documentation
- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md)
- [FULLSTACK_TRANSFORMATION_SUMMARY.md](./FULLSTACK_TRANSFORMATION_SUMMARY.md)

### External Links
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [Docker Docs](https://docs.docker.com/)
- [Kubernetes Docs](https://kubernetes.io/docs/)

### Support
- GitHub Issues: Create issue for bugs
- Discussions: Ask questions
- Wiki: Additional guides and tutorials

---

**Quick Reference Version**: 1.0  
**Last Updated**: 2025-01-17
