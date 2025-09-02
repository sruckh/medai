import os, json
from typing import List, Dict
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import httpx
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

PROVIDER = os.getenv("PROVIDER", "HF_TGI")
MODEL_NAME = os.getenv("MODEL_NAME", "Intelligent-Internet/II-Search-4B")

if PROVIDER == "HF_TGI":
    BASE_URL = (os.getenv("HF_API_BASE") or "").rstrip("/") + "/v1"
    API_KEY = os.getenv("HF_API_KEY")
    AUTH_HEADER = f"Bearer {API_KEY}"
elif PROVIDER == "RUNPOD_OPENAI":
    BASE_URL = (os.getenv("RUNPOD_API_BASE") or "").rstrip("/")
    API_KEY = os.getenv("RUNPOD_API_KEY")
    AUTH_HEADER = f"Bearer {API_KEY}"
else:
    raise RuntimeError("Unsupported PROVIDER")

DEFAULT_GEN = {
    "temperature": 0.6,
    "top_p": 0.95,
    "max_tokens": 8192,
    # You can add top_k or penalties if your provider supports them.
}

app = FastAPI(title="II-Search-4B Remote Chat")

app.mount("/static", StaticFiles(directory="static"), name="static")

allowed_origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
async def health():
    return {"ok": True, "provider": PROVIDER}

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    messages: List[Dict[str, str]] = body.get("messages", [])
    if not messages:
        raise HTTPException(400, "messages[] required")

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

    headers = {"Authorization": AUTH_HEADER, "Content-Type": "application/json"}

    async with httpx.AsyncClient(timeout=None) as client:
        url = BASE_URL
        resp = await client.post(url, headers=headers, json=payload)
        if resp.status_code != 200:
            text = await resp.aread()
            raise HTTPException(resp.status_code, text.decode("utf-8", "ignore"))
        response_data = resp.json()
        print(f"RunPod API Response: {response_data}")
        return response_data

@app.get("/", response_class=HTMLResponse)
async def index():
    here = os.path.dirname(__file__)
    with open(
        os.path.join(here, "static", "index.html"), "r", encoding="utf-8"
    ) as f:
        return f.read()
