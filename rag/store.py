"""PostgreSQL + pgvector: one table, vector and full-text indexes, hybrid search."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

import httpx
import psycopg

URL = os.getenv("RAG_DATABASE_URL", "postgresql://rag:rag@localhost:5562/rag")
OLLAMA = os.getenv("OLLAMA_URL", "http://localhost:11434")
EMBED_MODEL = os.getenv("EMBED_MODEL", "bge-m3")       # multilingual: Indonesian questions and English ones
DIM = 1024

DDL = f"""
CREATE EXTENSION IF NOT EXISTS vector;
DROP TABLE IF EXISTS chunks;
CREATE TABLE chunks (
    id text PRIMARY KEY, doc text, pasal text, part int, context text, history jsonb,
    text text, explanation text, embedding vector({DIM}),
    tsv tsvector GENERATED ALWAYS AS (to_tsvector('indonesian', coalesce(context, '') || ' ' || text)) STORED
);
CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON chunks USING gin (tsv);
"""


def embed(texts: list[str]) -> list[list[float]]:
    r = httpx.post(f"{OLLAMA}/api/embed", json={"model": EMBED_MODEL, "input": texts, "keep_alive": "20s"}, timeout=600)  # short stay: the 7B chat model needs the RAM
    r.raise_for_status()
    return r.json()["embeddings"]


def index(corpus: Path) -> int:
    from .corpus import Chunk
    chunks = [Chunk(**json.loads(l)) for l in corpus.read_text().splitlines() if l.strip()]
    vectors = []
    for i in range(0, len(chunks), 16):
        vectors += embed([c.for_embedding() for c in chunks[i:i + 16]])
    with psycopg.connect(URL) as conn:
        conn.execute(DDL)
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO chunks (id, doc, pasal, part, context, history, text, explanation, embedding) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::vector)",
                [(c.id, c.doc, c.pasal, c.part, c.context, json.dumps(c.history), c.text, c.explanation, str(v))
                 for c, v in zip(chunks, vectors)])
    return len(chunks)


REF = re.compile(r"pasal\s+(\d+[a-z]?)(?:.*?(?:pp|peraturan pemerintah)\s*(?:no\.?|nomor)?\s*(\d+)\s*(?:/|tahun)\s*(\d{4}))?", re.I)


def search(question: str, k: int = 6, pool: int = 25) -> list[dict]:
    """Hybrid retrieval: vector similarity and full-text rank, fused with reciprocal
    rank fusion (each list contributes 1 / (60 + rank)). An explicit "Pasal 27 PP 36/2021"
    in the question is fetched directly and put first."""
    qvec = str(embed([question])[0])
    with psycopg.connect(URL) as conn:
        cols = "id, doc, pasal, part, context, history, text, explanation"
        vec = conn.execute(f"SELECT {cols} FROM chunks ORDER BY embedding <=> %s::vector LIMIT %s", (qvec, pool)).fetchall()
        txt = conn.execute(f"""SELECT {cols} FROM chunks, websearch_to_tsquery('indonesian', %s) q
                               WHERE tsv @@ q ORDER BY ts_rank_cd(tsv, q) DESC LIMIT %s""", (question, pool)).fetchall()
        exact = []
        for m in REF.finditer(question):
            doc = f"PP {m.group(2)}/{m.group(3)}" if m.group(2) else None
            rows = conn.execute(f"SELECT {cols} FROM chunks WHERE pasal = %s" + (" AND doc = %s" if doc else "") + " ORDER BY part",
                                (m.group(1).upper(), doc) if doc else (m.group(1).upper(),)).fetchall()
            exact += rows if doc or len({r[1] for r in rows}) == 1 else []
    scores, rows = {}, {}
    for lst in (vec, txt):
        for rank, r in enumerate(lst):
            scores[r[0]] = scores.get(r[0], 0) + 1 / (60 + rank)
            rows[r[0]] = r
    ranked = [rows[i] for i in sorted(scores, key=scores.get, reverse=True)]
    seen, out = set(), []
    for r in exact + ranked:
        if r[0] not in seen:
            seen.add(r[0])
            out.append(dict(zip(["id", "doc", "pasal", "part", "context", "history", "text", "explanation"], r)))
    return out[:max(k, len(exact))]
