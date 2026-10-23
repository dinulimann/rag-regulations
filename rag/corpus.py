"""Sources → consolidated articles → chunks (one per article; long articles split by
paragraph or numbered item, each part keeping its heading)."""

from __future__ import annotations

import hashlib
import json
import re
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path

import yaml

from . import consolidate, parse

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
MAX_CHARS = 1800


@dataclass
class Chunk:
    id: str
    doc: str              # "PP 36/2021"
    pasal: str            # "27"
    part: int
    context: str          # "BAB V UPAH MINIMUM › Bagian Kedua Upah Minimum Provinsi"
    history: list[str]
    text: str
    explanation: str

    @property
    def label(self) -> str:
        return f"{self.doc} Pasal {self.pasal}"

    def for_embedding(self) -> str:
        e = "" if self.explanation.lower().startswith("cukup jelas") else f"\nPenjelasan: {self.explanation}"
        return f"{self.label}. {self.context}\n{self.text}{e}"


def fetch() -> None:
    """Downloads the PDFs once and checks they are the expected files."""
    RAW.mkdir(parents=True, exist_ok=True)
    for d in yaml.safe_load((ROOT / "sources.yml").read_text())["documents"]:
        for kind in ("body", "explanation"):
            if kind not in d:
                continue
            path = RAW / f"{d['id']}-{kind}.pdf"
            if not path.exists():
                req = urllib.request.Request(d[kind]["url"], headers={"User-Agent": "Mozilla/5.0"})
                path.write_bytes(urllib.request.urlopen(req, timeout=120).read())
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != d[kind]["sha256"]:
                raise SystemExit(f"{path.name}: checksum {digest} does not match sources.yml")


def text_of(doc_id: str, kind: str) -> str:
    return parse.pdf_text(RAW / f"{doc_id}-{kind}.pdf")


def split_long(text: str) -> list[str]:
    if len(text) <= MAX_CHARS:
        return [text]
    # split before "(2)" paragraphs or "12." numbered items at the start of a line
    pieces = re.split(r"\n(?=\(\d+[a-z]?\)\s|\d{1,2}\.\s)", text)
    parts, cur = [], ""
    for p in pieces:
        if cur and len(cur) + len(p) > MAX_CHARS:
            parts.append(cur)
            cur = p
        else:
            cur = f"{cur}\n{p}" if cur else p
    return parts + ([cur] if cur else [])


def flat(text: str) -> str:
    """Line breaks from the PDF layout → spaces, keeping paragraph and item starts."""
    text = re.sub(r"\s\d{4}, No\.\d+\b", "", text)                     # running header inside a sentence
    text = re.sub(r"\n(?!\(\d+[a-z]?\)\s|[a-z]\.\s|\d{1,2}\.\s)", " ", text)
    return re.sub(r"[ \t]+", " ", text).strip()


def articles() -> list[tuple[str, consolidate.Current]]:
    out = []
    for d in yaml.safe_load((ROOT / "sources.yml").read_text())["documents"]:
        if "amends" in d:
            continue
        label = re.sub(r"^(PP \d+/\d+).*", r"\1", d["title"])
        base = parse.split_articles(parse.clean_lines(text_of(d["id"], "body")), d["id"], r"^BAB I$", r"^Ditetapkan di")
        expl = {a.id: a.text for a in parse.split_articles(parse.clean_lines(text_of(d["id"], "explanation")), d["id"],
                                                           r"^II\.\s*PASAL DEMI PASAL")}
        amendments = []
        for am in d.get("amended_by", []):
            meta = next(x for x in yaml.safe_load((ROOT / "sources.yml").read_text())["documents"] if x["id"] == am)
            amendments.append((re.sub(r"^(PP \d+/\d+).*", r"\1", meta["title"]), text_of(am, "body")))
        out += [(label, a) for a in consolidate.consolidate(base, expl, amendments)]
    return out


def chunks() -> list[Chunk]:
    out = []
    for label, a in articles():
        if a.deleted:
            continue
        for n, part in enumerate(split_long(a.text), 1):
            out.append(Chunk(f"{label.replace(' ', '').replace('/', '-')}-{a.id}-{n}", label, a.id, n,
                             " › ".join(a.context), a.history, flat(part), flat(a.explanation)))
    return out


if __name__ == "__main__":
    fetch()
    cs = chunks()
    (ROOT / "data" / "corpus.jsonl").write_text("\n".join(json.dumps(asdict(c), ensure_ascii=False) for c in cs) + "\n")
    print(f"{len(cs)} chunks from {len({(c.doc, c.pasal) for c in cs})} articles in force "
          f"({sum(1 for c in cs if c.history and c.part == 1)} amended or inserted)")
