# Generative AI Training App

A FastAPI app using Pydantic AI's Agent to generate structured outputs from natural language prompts.

## Run locally
```bash
cp .env.local .env
uvicorn app.main:app --reload
```

## API
- `POST /generate`
  - Input: `{ "description": "something to organize" }`
  - Output: `{ "title": "...", "priority": "..." }`
```