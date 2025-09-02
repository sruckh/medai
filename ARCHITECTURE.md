# ARCHITECTURE.md

## Tech Stack
- **Language**: Python 3.11
- **Framework**: FastAPI (lines 3-4, 31)
- **Async HTTP**: HTTPX (line 6)
- **SSE Support**: sse-starlette (line 5)
- **CORS**: FastAPI CORSMiddleware (lines 4, 36-42)
- **Static Files**: FastAPI StaticFiles (lines 8, 33)
- **Containerization**: Docker + Docker Compose
- **Frontend**: Vanilla HTML/JavaScript (static/index.html)
- **Deployment**: VPS with Docker

## Directory Structure
```
medai/
├── api/                    # FastAPI application
│   ├── main.py            # Main application (85 lines)
│   ├── requirements.txt   # Python dependencies
│   └── static/            # Frontend assets
│       ├── index.html     # Chat interface
│       ├── ai-med-icon.svg # Application icon
│       └── *.css         # Stylesheets
├── infra/                 # Infrastructure & deployment
│   ├── .env              # Environment configuration
│   ├── .env.example      # Configuration template
│   ├── docker-compose.yml # Multi-service orchestration
│   └── Dockerfile.api    # API container definition
├── coordination/          # Multi-agent coordination
│   ├── memory_bank/      # Persistent memory storage
│   ├── orchestration/    # Task orchestration logic
│   └── subtasks/         # Subtask management
├── memory/               # Session and agent memory
│   ├── agents/           # Agent-specific memory
│   └── sessions/         # User session data
└── docs/                 # Documentation
    ├── *.md             # Project documentation
    └── JOURNAL.md       # Development changelog
```

## Key Architectural Decisions

### Provider Abstraction Pattern
**Context**: Need to support multiple LLM providers (Hugging Face TGI, RunPod vLLM) with different APIs
**Decision**: Environment-based provider switching with unified interface
**Rationale**: Allows seamless switching between providers without code changes
**Consequences**: Single deployment can serve different provider backends

### Stateless Proxy Design
**Context**: Chat application needs to handle concurrent users and maintain session state
**Decision**: Stateless proxy that forwards requests to external LLM providers
**Rationale**: Simplifies scaling and deployment, leverages provider infrastructure
**Consequences**: No local data persistence, all state managed by providers

### SSE for Real-time Communication
**Context**: Chat applications require real-time streaming responses
**Decision**: Server-Sent Events (SSE) for streaming LLM responses
**Rationale**: Native browser support, efficient for text streaming
**Consequences**: HTTP-only deployment, no WebSocket complexity

## Component Architecture

### Main Application (api/main.py) <!-- #main-app -->

#### FastAPI App Initialization (lines 31-42)
```python
app = FastAPI(title="II-Search-4B Remote Chat")  # line 31

app.mount("/static", StaticFiles(directory="static"), name="static")  # line 33

# CORS middleware configuration (lines 36-42)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Provider Configuration (lines 10-22)
```python
PROVIDER = os.getenv("PROVIDER", "HF_TGI")  # line 10
MODEL_NAME = os.getenv("MODEL_NAME", "Intelligent-Internet/II-Search-4B")  # line 11

# Provider-specific setup (lines 13-22)
if PROVIDER == "HF_TGI":
    BASE_URL = (os.getenv("HF_API_BASE") or "").rstrip("/") + "/v1"
    API_KEY = os.getenv("HF_API_KEY")
    AUTH_HEADER = f"Bearer {API_KEY}"
elif PROVIDER == "RUNPOD_OPENAI":
    BASE_URL = (os.getenv("RUNPOD_API_BASE") or "").rstrip("/")
    API_KEY = os.getenv("RUNPOD_API_KEY")
    AUTH_HEADER = f"Bearer {API_KEY}"
```

#### API Endpoints

##### Health Check (lines 44-46)
```python
@app.get("/healthz")  # line 44
async def health():
    return {"ok": True, "provider": PROVIDER}  # line 46
```

##### Chat Endpoint (lines 48-77)
```python
@app.post("/chat")  # line 48
async def chat(request: Request):
    # Request processing (lines 49-55)
    body = await request.json()
    messages: List[Dict[str, str]] = body.get("messages", [])

    # Generation config (lines 55-65)
    gen = {**DEFAULT_GEN, **body.get("generation_config", {})}
    payload = {
        "input": {
            "messages": messages,
            "sampling_params": {
                "max_tokens": gen.get("max_tokens"),
                "temperature": gen.get("temperature"),
                "top_p": gen.get("top_p"),
            }
        }
    }

    # HTTP request to provider (lines 67-77)
    headers = {"Authorization": AUTH_HEADER, "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=None) as client:
        resp = await client.post(url, headers=headers, json=payload)
        return resp.json()
```

##### Frontend Serving (lines 79-85)
```python
@app.get("/", response_class=HTMLResponse)  # line 79
async def index():
    # Serve static HTML file (lines 80-85)
    here = os.path.dirname(__file__)
    with open(os.path.join(here, "static", "index.html"), "r", encoding="utf-8") as f:
        return f.read()
```

## System Flow Diagram
```
[User Browser]
    ↓ (HTTP GET /)
[Static HTML/JS] ←─────────────────┐
    ↓ (POST /chat)                  │
[FastAPI Server] ──────────────────┼─→ [Health Check]
    ↓ (Provider-specific)          │     (GET /healthz)
[HTTPX Client] ────────────────────┘
    ↓
[LLM Provider]
    ↓
[Hugging Face TGI] or [RunPod vLLM]
    ↓
[Streaming Response]
    ↓
[SSE Stream] → [User Browser]
```

## Common Patterns

### Environment-Based Configuration
**When to use**: Multi-environment deployments (dev/staging/prod)
**Implementation**: Use `os.getenv()` with sensible defaults
**Example**:
```python
# api/main.py lines 10-11
PROVIDER = os.getenv("PROVIDER", "HF_TGI")
MODEL_NAME = os.getenv("MODEL_NAME", "Intelligent-Internet/II-Search-4B")
```

### Provider Abstraction
**When to use**: Supporting multiple external services with different APIs
**Implementation**: Conditional logic based on provider type
**Example**:
```python
# api/main.py lines 13-22
if PROVIDER == "HF_TGI":
    BASE_URL = os.getenv("HF_API_BASE") + "/v1"
    AUTH_HEADER = f"Bearer {os.getenv('HF_API_KEY')}"
elif PROVIDER == "RUNPOD_OPENAI":
    BASE_URL = os.getenv("RUNPOD_API_BASE")
    AUTH_HEADER = f"Bearer {os.getenv('RUNPOD_API_KEY')}"
```

### Async HTTP Client Usage
**When to use**: Making external API calls in FastAPI
**Implementation**: Use HTTPX AsyncClient with proper error handling
**Example**:
```python
# api/main.py lines 69-77
async with httpx.AsyncClient(timeout=None) as client:
    resp = await client.post(url, headers=headers, json=payload)
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, resp.text)
    return resp.json()
```

## Keywords <!-- #keywords -->
- fastapi
- llm proxy
- server-sent events
- hugging face
- runpod
- medical ai
- chat interface
- docker deployment
- provider abstraction
- async python