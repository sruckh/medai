# Configuration Guide

## Overview

MedAI uses environment-based configuration to manage settings across different deployment environments. All configuration is handled through environment variables to ensure security and flexibility.

## Environment Variables

### Core Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `PROVIDER` | LLM provider (`HF_TGI` or `RUNPOD_OPENAI`) | `HF_TGI` | Yes |
| `MODEL_NAME` | Model identifier | `Intelligent-Internet/II-Search-4B` | No |
| `ALLOWED_ORIGINS` | CORS allowed origins (comma-separated) | `*` | No |

### Hugging Face TGI Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `HF_API_BASE` | Base URL for Hugging Face TGI endpoint | Yes (if using HF_TGI) |
| `HF_API_KEY` | Hugging Face API key | Yes (if using HF_TGI) |

**Example:**
```bash
HF_API_BASE=https://your-endpoint.endpoints.huggingface.cloud
HF_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxx
```

### RunPod vLLM Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `RUNPOD_API_BASE` | Base URL for RunPod vLLM endpoint | Yes (if using RUNPOD_OPENAI) |
| `RUNPOD_API_KEY` | RunPod API key | Yes (if using RUNPOD_OPENAI) |

**Example:**
```bash
RUNPOD_API_BASE=https://api.runpod.ai/v2/endpoint-id/runsync
RUNPOD_API_KEY=rp_xxxxxxxxxxxxxxxxxxxxxxxxx
```

## Configuration Files

### .env (Local Development)
```bash
# Copy from template
cp infra/.env.example infra/.env

# Edit with your values
PROVIDER=HF_TGI
HF_API_BASE=https://your-endpoint.endpoints.huggingface.cloud
HF_API_KEY=hf_your_key_here
MODEL_NAME=Intelligent-Internet/II-Search-4B
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

### Docker Environment
```bash
# Docker Compose environment
cd infra
docker compose up --build

# Environment is read from .env file in infra directory
```

### Production Environment
```bash
# Set environment variables on your VPS
export PROVIDER=RUNPOD_OPENAI
export RUNPOD_API_BASE=https://api.runpod.ai/v2/your-endpoint/runsync
export RUNPOD_API_KEY=rp_your_production_key
export MODEL_NAME=Intelligent-Internet/II-Search-4B
export ALLOWED_ORIGINS=https://yourdomain.com
```

## Provider Switching

### Runtime Provider Selection
The application automatically selects the provider based on the `PROVIDER` environment variable:

```python
if PROVIDER == "HF_TGI":
    BASE_URL = f"{HF_API_BASE}/v1"
    AUTH_HEADER = f"Bearer {HF_API_KEY}"
elif PROVIDER == "RUNPOD_OPENAI":
    BASE_URL = RUNPOD_API_BASE
    AUTH_HEADER = f"Bearer {RUNPOD_API_KEY}"
```

### Switching Providers
To switch providers:
1. Update the `PROVIDER` environment variable
2. Set the appropriate provider-specific variables
3. Restart the application

## Security Considerations

### API Key Management
- ✅ Store API keys as environment variables only
- ✅ Never commit keys to version control
- ✅ Use different keys for dev/staging/production
- ❌ Never log API keys in application logs
- ❌ Never expose keys to frontend applications

### CORS Configuration
```python
# Development
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# Production
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### Environment Isolation
- Use separate API keys for each environment
- Different endpoints for dev/staging/production
- Restrictive CORS settings in production

## Advanced Configuration

### Model Parameters
```python
DEFAULT_GEN = {
    "temperature": 0.6,    # Controls randomness (0.0-1.0)
    "top_p": 0.95,         # Nucleus sampling (0.0-1.0)
    "max_tokens": 8192,    # Maximum response length
}
```

### HTTP Client Configuration
```python
# HTTPX client settings
timeout = None  # No timeout for long-running requests
headers = {
    "Authorization": AUTH_HEADER,
    "Content-Type": "application/json"
}
```

## Troubleshooting

### Common Configuration Issues

#### Provider Connection Failed
**Symptoms:** 401/403 errors
**Solution:**
```bash
# Check API key format
echo $HF_API_KEY  # Should start with 'hf_'
echo $RUNPOD_API_KEY  # Should start with 'rp_'

# Verify endpoint URL
curl -H "Authorization: Bearer $HF_API_KEY" $HF_API_BASE/health
```

#### CORS Errors
**Symptoms:** Browser blocks API requests
**Solution:**
```bash
# Update ALLOWED_ORIGINS
export ALLOWED_ORIGINS="https://yourdomain.com"

# Restart application
docker compose restart
```

#### Environment Variables Not Loaded
**Symptoms:** Application uses default values
**Solution:**
```bash
# Check if .env file exists
ls -la infra/.env

# Verify variable values
cat infra/.env | grep PROVIDER

# Restart with new environment
docker compose down && docker compose up --build
```

## Environment-Specific Configurations

### Development
```bash
# .env
PROVIDER=HF_TGI
HF_API_BASE=https://your-dev-endpoint.endpoints.huggingface.cloud
HF_API_KEY=hf_dev_key
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

### Staging
```bash
# .env.staging
PROVIDER=HF_TGI
HF_API_BASE=https://your-staging-endpoint.endpoints.huggingface.cloud
HF_API_KEY=hf_staging_key
ALLOWED_ORIGINS=https://staging.yourdomain.com
```

### Production
```bash
# .env.prod
PROVIDER=RUNPOD_OPENAI
RUNPOD_API_BASE=https://api.runpod.ai/v2/prod-endpoint/runsync
RUNPOD_API_KEY=rp_prod_key
ALLOWED_ORIGINS=https://yourdomain.com
```

## Keywords <!-- #keywords -->
- configuration
- environment variables
- api keys
- providers
- cors
- security
- deployment