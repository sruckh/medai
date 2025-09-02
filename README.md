# MedAI - Intelligent Internet Search Chat Interface

A sophisticated FastAPI-based Server-Sent Events (SSE) proxy that enables seamless switching between multiple Large Language Model (LLM) providers for intelligent chat applications. Built specifically for medical AI assistance with the Intelligent-Internet/II-Search-4B model.

## 🚀 Features

- **Multi-Provider Support**: Switch between Hugging Face Text Generation Inference (TGI) and RunPod vLLM endpoints
- **Real-time Streaming**: Server-Sent Events for responsive chat interactions
- **Medical AI Focus**: Optimized for healthcare and medical query processing
- **Docker Deployment**: Containerized for easy VPS deployment
- **CORS Enabled**: Configurable cross-origin resource sharing
- **Health Monitoring**: Built-in health check endpoints
- **Environment-Based Configuration**: Secure API key management

## 🏗️ Architecture

### Core Components
- **FastAPI Backend** (`api/main.py`): Main application server with SSE proxy logic
- **Provider Abstraction**: Unified interface for different LLM providers
- **Static Frontend**: Simple HTML/JavaScript chat interface
- **Docker Infrastructure**: Containerized deployment with docker-compose

### Supported Providers
- **Hugging Face TGI**: Open-source inference server for transformer models
- **RunPod vLLM**: High-performance LLM inference with OpenAI-compatible API

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose
- API access to either Hugging Face or RunPod
- VPS or cloud instance for deployment

## 🛠️ Quick Start

### Local Development

1. **Clone and navigate**:
   ```bash
   git clone <repository-url>
   cd medai
   ```

2. **Set up environment**:
   ```bash
   cd infra
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

3. **Run locally**:
   ```bash
   # Install dependencies
   pip install -r api/requirements.txt

   # Run the application
   cd api
   python main.py
   ```

4. **Access the interface**:
   Open `http://localhost:8000` in your browser

### Docker Deployment

1. **Navigate to infrastructure**:
   ```bash
   cd infra
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your production settings
   ```

3. **Deploy with Docker**:
   ```bash
   docker compose up -d --build
   ```

4. **Access production**:
   Visit `http://<your-vps>:8080`

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PROVIDER` | LLM provider (`HF_TGI` or `RUNPOD_OPENAI`) | `HF_TGI` |
| `MODEL_NAME` | Model identifier | `Intelligent-Internet/II-Search-4B` |
| `HF_API_BASE` | Hugging Face TGI endpoint URL | Required for HF_TGI |
| `HF_API_KEY` | Hugging Face API key | Required for HF_TGI |
| `RUNPOD_API_BASE` | RunPod vLLM endpoint URL | Required for RUNPOD_OPENAI |
| `RUNPOD_API_KEY` | RunPod API key | Required for RUNPOD_OPENAI |
| `ALLOWED_ORIGINS` | CORS allowed origins | `*` |

### Provider-Specific Setup

#### Hugging Face TGI
```bash
PROVIDER=HF_TGI
HF_API_BASE=https://your-endpoint.endpoints.huggingface.cloud
HF_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxx
```

#### RunPod vLLM
```bash
PROVIDER=RUNPOD_OPENAI
RUNPOD_API_BASE=https://api.runpod.ai/v2/endpoint-id/runsync
RUNPOD_API_KEY=rp_xxxxxxxxxxxxxxxxxxxxxxxxx
```

## 🔌 API Endpoints

### `GET /healthz`
Health check endpoint returning provider status.

**Response**:
```json
{
  "ok": true,
  "provider": "HF_TGI"
}
```

### `POST /chat`
Main chat endpoint for LLM interactions.

**Request**:
```json
{
  "messages": [
    {"role": "user", "content": "Hello, how can you help with medical queries?"}
  ],
  "generation_config": {
    "temperature": 0.6,
    "top_p": 0.95,
    "max_tokens": 8192
  }
}
```

**Response**:
```json
{
  "output": {
    "text": "I can assist with medical information, research, and analysis...",
    "finish_reason": "stop"
  }
}
```

### `GET /`
Serves the main chat interface HTML page.

## 🐳 Docker Configuration

### Services
- **api**: FastAPI application server
- **nginx** (optional): Reverse proxy for production

### Build Configuration
- Python 3.11 slim base image
- Multi-stage build for optimized image size
- Non-root user for security

## 🔒 Security Considerations

- API keys are stored as environment variables
- No keys are exposed to the frontend
- CORS configuration for controlled access
- Docker container isolation

## 📊 Monitoring

- Health endpoint for service monitoring
- Structured logging for debugging
- Error handling with appropriate HTTP status codes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Intelligent-Internet/II-Search-4B model for medical AI capabilities
- FastAPI framework for the robust API foundation
- Hugging Face and RunPod for LLM inference infrastructure