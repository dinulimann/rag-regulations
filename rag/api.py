"""uvicorn rag.api:app  →  http://localhost:8000"""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from . import answer

app = FastAPI(title="Tanya Peraturan Ketenagakerjaan")
PAGE = (Path(__file__).parent / "page.html").read_text()


class Question(BaseModel):
    question: str = Field(min_length=3, max_length=500)


@app.get("/", response_class=HTMLResponse)
def page() -> str:
    return PAGE


@app.post("/api/ask")
def ask(q: Question) -> dict:
    try:
        return answer.ask(q.question)
    except Exception as err:   # model or database down: say so, never invent an answer
        raise HTTPException(503, f"service unavailable: {type(err).__name__}") from err
