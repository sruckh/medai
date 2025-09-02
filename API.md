# API Documentation

## Overview

MedAI provides a RESTful API for interacting with Large Language Models through a unified interface that supports multiple providers (Hugging Face TGI and RunPod vLLM).

## Base URL
```
http://localhost:8000  # Development
http://your-vps:8080   # Production
```

## Authentication

The API uses Bearer token authentication via environment variables. API keys are configured server-side and never exposed to clients.

## Endpoints

### GET /healthz

Health check endpoint that returns the current provider status.

**Response:**
```json
{
  "ok": true,
  "provider": "HF_TGI"
}
```

**Status Codes:**
- `200` - Service is healthy
- `500` - Service is unhealthy

### POST /chat

Main chat endpoint for processing messages through the configured LLM provider.

**Request Body:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "What are the symptoms of diabetes?"
    }
  ],
  "generation_config": {
    "temperature": 0.6,
    "top_p": 0.95,
    "max_tokens": 8192
  }
}
```

**Parameters:**
- `messages` (required): Array of message objects with `role` and `content`
- `generation_config` (optional): Configuration for text generation
  - `temperature`: Controls randomness (0.0 to 1.0)
  - `top_p`: Nucleus sampling parameter (0.0 to 1.0)
  - `max_tokens`: Maximum tokens to generate

**Response:**
```json
{
  "output": {
    "text": "Diabetes symptoms include frequent urination, excessive thirst, fatigue, slow-healing sores, and unexplained weight loss...",
    "finish_reason": "stop"
  }
}
```

**Status Codes:**
- `200` - Successful response
- `400` - Invalid request format
- `401` - Authentication failed
- `500` - Internal server error

### GET /

Serves the main chat interface HTML page.

**Response:** HTML page with chat interface

## Error Handling

All errors follow a consistent format:

```json
{
  "detail": "Error message description"
}
```

## Rate Limiting

Currently no rate limiting is implemented. Consider implementing for production use.

## Examples

### Basic Chat Request
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello, how can you help with medical questions?"}]
  }'
```

### Health Check
```bash
curl http://localhost:8000/healthz
```

## Provider-Specific Behavior

### Hugging Face TGI
- Uses `/v1/chat/completions` endpoint
- Supports standard OpenAI-compatible parameters
- Optimized for the Intelligent-Internet/II-Search-4B model

### RunPod vLLM
- Uses custom endpoint format
- Supports streaming responses
- Compatible with OpenAI API format

## WebSocket Support

Future enhancement may include WebSocket support for real-time streaming.

## Keywords <!-- #keywords -->
- api
- endpoints
- rest
- fastapi
- llm
- chat
- medical ai
- documentation