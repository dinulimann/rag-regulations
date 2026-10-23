"""Question → retrieved articles → answer from a local model, with citations that are
checked against what was actually retrieved."""

from __future__ import annotations

import json
import os
import re
import time

import httpx

from . import store

OLLAMA = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("CHAT_MODEL", "qwen2.5:7b")
SCOPE = "PP 35/2021 dan PP 36/2021 (sebagaimana diubah PP 51/2023 dan PP 49/2025)"

SYSTEM = f"""You answer questions about Indonesian employment regulations: {SCOPE}.
Use ONLY the numbered sources given. Never use outside knowledge, even if you know the answer.
- Answer in the same language as the question (Indonesian or English).
- Be specific: give the numbers, durations and conditions exactly as the source says.
- After each statement, cite the source number in square brackets, e.g. [S1] or [S2][S4]. Use only the numbers shown.
- If an article was amended, say so, e.g. "(diubah oleh PP 49/2025)".
- Answer only what the sources actually state. If a source mentions a similar but different case (for example a
  husband's leave when his wife gives birth, while the question is about the mother), it does not answer the question.
  A topic being listed without the number asked for (for example a type of leave without its length) is also not an answer.
- If the sources do not contain the answer, reply with exactly NOT_FOUND on the first line, then one sentence
  saying the answer is not in these regulations. Do not guess and do not answer from general knowledge.
- Keep the answer short: at most a few sentences or a short list."""

ID_WORDS = {"apa", "berapa", "bagaimana", "apakah", "siapa", "kapan", "yang", "dan", "untuk", "dengan", "pekerja",
            "upah", "dalam", "jika", "boleh", "harus", "wajib", "tidak", "berapakah"}

LABEL = re.compile(r"PP\s*(\d+)/(\d{4})\s*Pasal\s*(\d+[A-Z]?)", re.I)


def label(r: dict) -> str:
    return f"{r['doc']} Pasal {r['pasal']}"


def context(results: list[dict]) -> str:
    blocks = []
    for i, r in enumerate(results, 1):
        hist = r["history"] if isinstance(r["history"], list) else json.loads(r["history"] or "[]")
        note = f" ({'; '.join(hist)})" if hist else ""
        expl = "" if (r["explanation"] or "").lower().startswith("cukup jelas") or not r["explanation"] else \
            f"\nPenjelasan: {r['explanation']}"
        blocks.append(f"[S{i}] {label(r)}{note} · {r['context']}\n{r['text']}{expl}")
    return "\n\n".join(blocks)


def language(question: str) -> str:
    words = set(re.findall(r"[a-z]+", question.lower()))
    return "Indonesian" if len(words & ID_WORDS) >= 1 else "English"


def ask(question: str, k: int = 6) -> dict:
    """Plain-text answer (JSON mode makes small local models loop on whitespace), capped in
    length; citations are read from the [PP x/yyyy Pasal n] labels in the text."""
    t0 = time.monotonic()
    results = store.search(question, k=k)
    retrieved = {label(r) for r in results}
    lang = language(question)
    resp = httpx.post(f"{OLLAMA}/api/chat", timeout=600, json={
        "model": MODEL, "stream": False, "options": {"temperature": 0, "num_ctx": 6144, "num_predict": 500},
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": f"Sources:\n\n{context(results)}\n\nQuestion: {question}\n\n"
                                                 f"Answer in {lang}, citing sources as [S1], [S2]…"}]})
    resp.raise_for_status()
    text = resp.json()["message"]["content"].strip()
    found = not text.upper().startswith("NOT_FOUND")
    text = re.sub(r"^NOT_FOUND\s*", "", text, flags=re.I).strip()
    # The model cites short source tags ([S2]), which small models copy reliably; code turns them into article
    # labels. Tags that don't exist and article labels the model typed itself are checked against what was retrieved.
    # small models sometimes drop the S: "[2]" is read as "[S2]" (article numbers never appear alone in brackets)
    text = re.sub(r"\[(\d{1,2})\]", r"[S\1]", text)
    tags = {int(n) for n in re.findall(r"\[S(\d+)\]", text)}
    cited = {label(results[n - 1]) for n in tags if 1 <= n <= len(results)}
    bad_tags = {f"S{n}" for n in tags if not 1 <= n <= len(results)}
    text = re.sub(r"\[S(\d+)\]", lambda m: f"[{label(results[int(m.group(1)) - 1])}]" if 1 <= int(m.group(1)) <= len(results)
                  else "", text)
    cited |= {f"PP {m.group(1)}/{m.group(2)} Pasal {m.group(3).upper()}" for m in LABEL.finditer(text)}
    if not found:
        cited = set()
    return {"question": question, "language": lang, "found": found, "answer": text,
            "citations": sorted(cited & retrieved), "unsupported_citations": sorted((cited - retrieved) | bad_tags),
            "sources": [{"label": label(r), "context": r["context"], "history": r["history"], "text": r["text"]} for r in results],
            "seconds": round(time.monotonic() - t0, 1), "model": MODEL}
