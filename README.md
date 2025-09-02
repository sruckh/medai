# II-Search-Remote-Chat

This project implements a FastAPI-based SSE proxy for switching between different LLM providers (Hugging Face TGI or RunPod vLLM) for a chat application.

## Running the application

1.  Navigate to the `infra` directory: `cd infra`
2.  Copy the example environment file: `cp .env.example .env`
3.  Edit the `.env` file with your provider settings.
4.  Build and run the application: `docker compose up -d --build`
5.  Access the application at `http://<your-vps>:8080`.