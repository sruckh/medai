# BUILD.md

## Prerequisites
- **Python**: 3.11 or higher
- **Docker**: 20.10+ with Docker Compose
- **API Access**: Hugging Face or RunPod account with API keys
- **System**: Linux VPS or cloud instance (Ubuntu 20.04+ recommended)
- **Memory**: Minimum 2GB RAM for development, 4GB+ for production
- **Storage**: 10GB+ free space for Docker images and dependencies

## Local Development Setup

### 1. Clone and Environment Setup
```bash
# Clone repository
git clone <repository-url>
cd medai

# Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r api/requirements.txt
```

### 2. Environment Configuration
```bash
# Copy environment template
cp infra/.env.example infra/.env

# Edit with your API keys
nano infra/.env  # or your preferred editor
```

### 3. Run Development Server
```bash
# From project root
cd api
python main.py

# Or run with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access Development Interface
- **API**: http://localhost:8000
- **Health Check**: http://localhost:8000/healthz
- **Chat Interface**: http://localhost:8000/

## Docker Development

### Build and Run Locally
```bash
# From infra directory
cd infra

# Build and run with docker-compose
docker compose up --build

# Or build and run in background
docker compose up -d --build

# View logs
docker compose logs -f api
```

### Development with Hot Reload
```bash
# Use docker-compose for development
cd infra
docker compose -f docker-compose.dev.yml up --build
```

## Production Deployment

### VPS Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Add Python PPA
sudo add-apt-repository ppa:fkrull/deadsnakes -y
sudo apt update

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3.11-pip -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository
git clone <repository-url>
cd medai/infra
```

### Production Configuration
```bash
# Copy production environment
cp .env.example .env

# Edit with production settings
nano .env

# Key production settings:
# - Set production API endpoints
# - Configure ALLOWED_ORIGINS for security
# - Set appropriate MODEL_NAME
```

### Deploy to Production
```bash
# Build and deploy
docker compose -f docker-compose.prod.yml up -d --build

# Verify deployment
curl http://localhost:8080/healthz
curl http://your-vps-ip:8080/healthz
```

## CI/CD Pipeline

### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production
on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd api
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd api
          python -m pytest  # Add tests when implemented

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to VPS
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd /path/to/medai/infra
            git pull origin main
            docker compose -f docker-compose.prod.yml up -d --build
```

## Testing

### Current Test Setup
```bash
# No automated tests implemented yet
# Recommended test structure:

# Install test dependencies
pip install pytest httpx pytest-asyncio

# Run API tests
cd api
pytest tests/

# Test health endpoint
curl http://localhost:8000/healthz

# Test chat endpoint with sample data
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello"}]}'
```

### Future Test Implementation
```python
# tests/test_api.py
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {"ok": True, "provider": "HF_TGI"}
```

## Deployment Strategies

### Blue-Green Deployment
```bash
# Deploy new version alongside old
docker compose -f docker-compose.green.yml up -d --build

# Test green environment
curl http://localhost:8081/healthz

# Switch traffic (if using reverse proxy)
# docker compose -f docker-compose.blue.yml down

# Clean up old version
# docker system prune -f
```

### Rolling Updates
```bash
# Update with zero downtime
docker compose up -d --build --scale api=2

# Gradually reduce old instances
docker compose up -d --build --scale api=1
```

## Monitoring & Troubleshooting

### Health Checks
```bash
# Check API health
curl http://localhost:8080/healthz

# Check Docker containers
docker ps

# View application logs
docker compose logs -f api

# Check resource usage
docker stats
```

### Common Issues

#### API Key Issues
**Symptoms**: 401/403 errors from provider
**Solution**:
```bash
# Check environment variables
cat infra/.env | grep API_KEY

# Verify API key format
# HF keys start with 'hf_'
# RunPod keys start with 'rp_'
```

#### CORS Issues
**Symptoms**: Browser blocks requests
**Solution**:
```bash
# Update ALLOWED_ORIGINS in .env
# For development: ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
# For production: ALLOWED_ORIGINS=https://yourdomain.com
```

#### Port Conflicts
**Symptoms**: Container fails to start
**Solution**:
```bash
# Check port usage
sudo netstat -tulpn | grep :8080

# Stop conflicting service or change port in docker-compose.yml
```

#### Memory Issues
**Symptoms**: Container crashes with OOM
**Solution**:
```bash
# Increase Docker memory limit
# Or optimize model parameters (reduce max_tokens)
# Or use smaller model variant
```

### Performance Optimization
```bash
# Enable Docker build cache
docker build --no-cache=false .

# Use multi-stage builds for smaller images
# Optimize Python dependencies
pip install --no-cache-dir -r requirements.txt

# Monitor resource usage
docker stats
```

## Rollback Procedures

### Emergency Rollback
```bash
# Stop current deployment
cd infra
docker compose down

# Revert to previous commit
git checkout HEAD~1

# Redeploy previous version
docker compose up -d --build
```

### Database Rollback (Future)
```bash
# If database is added in future:
# docker exec -it medai-db-1 pg_dump > backup.sql
# docker exec -it medai-db-1 psql -f backup.sql
```

## Security Checklist

- [ ] API keys stored as environment variables
- [ ] No secrets in Docker images
- [ ] CORS properly configured
- [ ] HTTPS enabled in production
- [ ] Regular dependency updates
- [ ] Minimal base Docker images used

## Keywords <!-- #keywords -->
- python
- fastapi
- docker
- deployment
- ci/cd
- testing
- production
- vps
- api keys
- monitoring
- troubleshooting