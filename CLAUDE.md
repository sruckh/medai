# MedAI - Development Guidelines & Best Practices

## 🏥 Project Overview

MedAI is a sophisticated FastAPI-based Server-Sent Events (SSE) proxy that enables seamless switching between multiple Large Language Model (LLM) providers for intelligent medical chat applications. The system supports both Hugging Face TGI and RunPod vLLM endpoints with the specialized Intelligent-Internet/II-Search-4B model.

## 🎯 Development Philosophy

### Core Principles
- **Medical Focus**: All features prioritize healthcare and medical query processing
- **Provider Agnostic**: Seamless switching between LLM providers without code changes
- **Real-time Streaming**: Server-Sent Events for responsive chat interactions
- **Security First**: API keys never exposed to frontend, environment-based configuration
- **Docker Native**: Containerized deployment for consistent environments

### Code Quality Standards
- **Type Hints**: Full Python type annotations for better IDE support
- **Async/Await**: Proper asynchronous patterns throughout the codebase
- **Error Handling**: Comprehensive exception handling with meaningful messages
- **Documentation**: Inline comments and docstrings for all functions
- **Testing**: Unit tests for critical paths (when implemented)

## 🏗️ Architecture Guidelines

### Component Structure
```
api/main.py (85 lines) - Core application logic
├── Provider abstraction (lines 10-22)
├── FastAPI app setup (lines 31-42)
├── Health endpoint (lines 44-46)
├── Chat endpoint (lines 48-77)
└── Static file serving (lines 79-85)
```

### Key Design Patterns

#### Provider Switching Pattern
```python
# Environment-based provider selection
PROVIDER = os.getenv("PROVIDER", "HF_TGI")

if PROVIDER == "HF_TGI":
    BASE_URL = f"{os.getenv('HF_API_BASE')}/v1"
    AUTH_HEADER = f"Bearer {os.getenv('HF_API_KEY')}"
elif PROVIDER == "RUNPOD_OPENAI":
    BASE_URL = os.getenv("RUNPOD_API_BASE")
    AUTH_HEADER = f"Bearer {os.getenv('RUNPOD_API_KEY')}"
```

#### Async HTTP Client Pattern
```python
# Proper async HTTP handling
async with httpx.AsyncClient(timeout=None) as client:
    resp = await client.post(url, headers=headers, json=payload)
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, resp.text)
    return resp.json()
```

## 🔧 Development Workflow

### Local Development Setup
```bash
# 1. Environment setup
python3 -m venv venv
source venv/bin/activate
pip install -r api/requirements.txt

# 2. Configuration
cp infra/.env.example infra/.env
# Edit .env with your API keys

# 3. Run development server
cd api && python main.py
```

### Docker Development
```bash
# Build and run locally
cd infra && docker compose up --build

# Development with hot reload
docker compose -f docker-compose.dev.yml up --build
```

### Testing Protocol
```bash
# Health check
curl http://localhost:8000/healthz

# Chat endpoint test
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello"}]}'
```

## 🚀 Deployment Standards

### Production Checklist
- [ ] Environment variables configured for production endpoints
- [ ] CORS settings restricted to production domains
- [ ] Docker images built with production optimizations
- [ ] Health checks passing
- [ ] Logs configured for production monitoring

### VPS Deployment
```bash
# Production deployment
cd infra
docker compose -f docker-compose.prod.yml up -d --build

# Verify deployment
curl http://your-vps:8080/healthz
```

## 🔒 Security Guidelines

### API Key Management
- ✅ Store in environment variables only
- ✅ Never commit to version control
- ✅ Use different keys for dev/staging/production
- ❌ Never log API keys
- ❌ Never send to frontend

### CORS Configuration
```python
# Production CORS settings
allowed_origins = ["https://yourdomain.com", "https://app.yourdomain.com"]
```

### Input Validation
- Validate all user inputs
- Sanitize messages before sending to LLM
- Implement rate limiting (future enhancement)
- Log suspicious activity

## 📊 Performance Optimization

### Current Metrics
- **Response Time**: < 2 seconds for typical queries
- **Concurrent Users**: Supports multiple simultaneous sessions
- **Memory Usage**: ~200MB base + model overhead
- **CPU Usage**: Minimal for proxy operations

### Optimization Strategies
- Use HTTPX connection pooling
- Implement response caching for common queries
- Optimize Docker image size
- Monitor and tune model parameters

## 🧪 Testing Strategy

### Unit Testing (Future Implementation)
```python
# Example test structure
def test_provider_switching():
    # Test HF_TGI provider setup
    # Test RunPod provider setup
    # Test invalid provider handling

def test_chat_endpoint():
    # Test valid message format
    # Test error handling
    # Test streaming responses
```

### Integration Testing
- API endpoint functionality
- Provider switching logic
- Error handling scenarios
- CORS behavior

## 📝 Documentation Standards

### Code Documentation
```python
async def chat(request: Request) -> Dict[str, Any]:
    """
    Process chat messages through configured LLM provider.

    Args:
        request: FastAPI request containing messages and config

    Returns:
        Dict containing LLM response

    Raises:
        HTTPException: For invalid requests or provider errors
    """
```

### API Documentation
- OpenAPI/Swagger integration (future)
- Request/response examples
- Error code documentation
- Rate limiting information

## 🔄 Version Control Best Practices

### Commit Message Format
```
feat: add provider switching capability
fix: handle API timeout errors gracefully
docs: update deployment instructions
refactor: simplify CORS middleware setup
```

### Branch Strategy
- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: New features
- `hotfix/*`: Critical bug fixes

## 🚨 Error Handling

### Application Errors
- **400 Bad Request**: Invalid message format
- **401 Unauthorized**: Invalid API key
- **500 Internal Server Error**: Provider or system errors
- **503 Service Unavailable**: Provider downtime

### Logging Strategy
```python
# Structured logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log important events
logger.info(f"Chat request processed for provider: {PROVIDER}")
logger.error(f"Provider error: {error_message}")
```

## 🔮 Future Enhancements

### Planned Features
- [ ] User session management
- [ ] Chat history persistence
- [ ] Multiple model support
- [ ] Rate limiting
- [ ] Request/response caching
- [ ] Advanced error recovery
- [ ] Metrics and monitoring dashboard

### Technical Debt
- [ ] Add comprehensive test suite
- [ ] Implement request validation middleware
- [ ] Add response caching layer
- [ ] Improve error messages
- [ ] Add health check for provider endpoints

## 🤝 Contributing Guidelines

### Code Review Process
1. Create feature branch from `develop`
2. Implement changes with tests
3. Submit pull request with description
4. Code review and approval
5. Merge to `develop` then `main`

### Code Style
- Follow PEP 8 Python style guide
- Use type hints for all function parameters
- Write descriptive variable names
- Keep functions under 50 lines
- Add docstrings to all public functions

## 📞 Support & Resources

### Key Contacts
- **Technical Lead**: [Contact information]
- **DevOps**: [Contact information]
- **Security**: [Contact information]

### Useful Links
- [Hugging Face TGI Documentation](https://huggingface.co/docs/text-generation-inference)
- [RunPod API Documentation](https://docs.runpod.ai)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [HTTPX Documentation](https://www.python-httpx.org)

---

## Keywords <!-- #keywords -->
- medai
- medical ai
- fastapi
- llm proxy
- hugging face
- runpod
- server-sent events
- docker deployment
- api security
- async python
- healthcare ai
- chat interface
