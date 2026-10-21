from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from openai import AzureOpenAI
from pydantic import BaseModel, Field

import config
import memory
import policy

SYSTEM_PROMPT = (
    "You are the Unilever HR Assistant. Answer ONLY using the HR policy excerpts below. "
    "If the answer is not in the excerpts, say you don't know and suggest contacting the HR team. "
    "Be concise and friendly.\n\nPolicy excerpts:\n{context}"
)

client = AzureOpenAI(
    azure_endpoint=config.AZURE_OPENAI_ENDPOINT or "https://example.openai.azure.com/",
    api_key=config.AZURE_OPENAI_KEY or "missing",
    api_version=config.API_VERSION,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Loaded {policy.load_policy()} policy chunks")
    yield


app = FastAPI(lifespan=lifespan)


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=64)
    message: str = Field(min_length=1, max_length=config.MAX_MESSAGE_CHARS)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat")
def chat(req: ChatRequest):
    context = "\n---\n".join(policy.search(req.message)) or "(no relevant excerpts found)"
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
        *memory.get_history(req.session_id),
        {"role": "user", "content": req.message},
    ]
    try:
        resp = client.chat.completions.create(
            model=config.AZURE_OPENAI_DEPLOYMENT,
            messages=messages,
            temperature=0.2,
            max_tokens=400,
        )
        reply = resp.choices[0].message.content
    except Exception as exc:
        print(f"LLM error: {exc}")
        return {"reply": "Sorry, I'm having trouble right now. Please try again shortly."}
    memory.add_turn(req.session_id, req.message, reply)
    return {"reply": reply}


# Must be last so /api routes win.
app.mount("/", StaticFiles(directory=config.FRONTEND_DIR, html=True), name="frontend")
