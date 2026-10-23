"""Regulation text → articles (Pasal) with their chapter context and explanation.

The base regulations have a clean digital text layer; the two amendments are
OCR'd scans, so article numbers like "Pasal 2l", "Pasal 26E}" or "Pasal 351"
are repaired, and page furniture (headers, page numbers, "continued on next
page" markers) is removed before anything else.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

ROMAN = {"I", "II", "III"}
NOISE = [
    re.compile(r"^(PRESIDEN|FRESIDEN|PRES\s*I\s*DEN)$", re.I),
    re.compile(r"^REPUB\S*\s*\S*INDONESIA\.?$", re.I),
    re.compile(r"^SK No\.? ?\d+ ?A$", re.I),
    re.compile(r"^-\s*\d+\s*-?$"),                                  # page number
    re.compile(r"^\d{4}, No\.\s?\d+\s*(-\d+-)?$"),                  # "2021, No.46 -2-" / "2021, No.45"
    re.compile(r"^No\.\s?\d+\s*-\d+-$"),                            # "No. 6648 -2-"
    re.compile(r"^(www\.|jdih\.)", re.I),
]
CONTINUED = re.compile(r"(\.\s?\.\s?\.|…)$")                         # "6. Ketentuan . . ."


def pdf_text(pdf: Path) -> str:
    return subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, check=True).stdout


def clean_lines(text: str) -> list[str]:
    out = []
    for raw in text.splitlines():
        line = re.sub(r"\s+", " ", raw).strip()
        if not line or any(p.match(line) for p in NOISE):
            continue
        if CONTINUED.search(line) and len(line) < 40:              # page-break marker, repeated on the next page
            continue
        out.append(line)
    return out


def norm_id(raw: str, max_base: int = 200) -> str | None:
    """'2l' → '21', 't7' → '17', '26E}' → '26B', '351' → '35I' (when 351 can't exist)."""
    s = raw.strip()
    if s in ROMAN:
        return s
    s = s.replace("E}", "B").replace("El", "B").rstrip("}")
    m = re.fullmatch(r"([0-9lItOo]+)([A-Za-z]?)", s)
    if not m:
        return None
    num = m.group(1).translate(str.maketrans("lItOo", "11100"))
    suffix = m.group(2).upper()
    if not suffix and int(num) > max_base and num.endswith("1"):  # "351" read for "35I"
        num, suffix = num[:-1], "I"
    return f"{int(num)}{suffix}"


PASAL = re.compile(r"^Pas[ae][lJ1]\s*([0-9A-Za-z}]+)$")   # "PaseJ 27" happens too
HEAD = re.compile(r"^(BAB|Bagian|Paragraf)\s+(\S+)$")


@dataclass
class Article:
    doc: str
    id: str
    text: str
    context: list[str] = field(default_factory=list)     # ["BAB V KEBIJAKAN PENGUPAHAN", "Bagian Kesatu Upah Minimum"]


def split_articles(lines: list[str], doc: str, start: str | None = None, stop: str | None = None) -> list[Article]:
    """Articles between the first line matching `start` and the first matching `stop`."""
    if start:
        lines = lines[next(i for i, l in enumerate(lines) if re.match(start, l)):]
    if stop:
        lines = lines[:next((i for i, l in enumerate(lines) if re.match(stop, l)), len(lines))]
    out, ctx, cur, i = [], {}, None, 0
    while i < len(lines):
        line = lines[i]
        h = HEAD.match(line)
        if h and i + 1 < len(lines):
            level = {"BAB": 0, "Bagian": 1, "Paragraf": 2}[h.group(1)]
            ctx = {k: v for k, v in ctx.items() if k < level}
            title, j = lines[i + 1], i + 2
            # chapter titles in capitals can run over two lines
            while level == 0 and j < len(lines) and lines[j].isupper() and not PASAL.match(lines[j]) and not HEAD.match(lines[j]):
                title, j = f"{title} {lines[j]}", j + 1
            ctx[level] = f"{line} {title}"
            i = j
            continue
        p = PASAL.match(line)
        pid = norm_id(p.group(1)) if p else None
        if pid:
            cur = Article(doc, pid, "", [ctx[k] for k in sorted(ctx)])
            out.append(cur)
        elif cur is not None:
            cur.text += ("\n" if cur.text else "") + line
        i += 1
    return out


# Words the OCR of the two amendment scans gets wrong, found by reading the output.
OCR_WORDS = {"Minirium": "Minimum", "kabupatenf kota": "kabupaten/kota", "kabupaten/ kota": "kabupaten/kota",
             "dimalsud": "dimaksud", "rrrmah": "rumah", "hur-uf": "huruf", "hurrrf": "huruf", "Bagran": "Bagian",
             "ketenagakerj aan": "ketenagakerjaan", "bedalan": "berjalan", "2I November": "21 November",
             "fikfjFIIEM": "", "menJrusun": "menyusun"}


def repair_ayat(text: str) -> str:
    """OCR: '(41' → '(4)', '(21' → '(2)', '(l)' → '(1)', '(la)' → '(1a)', plus known word errors."""
    for bad, good in OCR_WORDS.items():
        text = text.replace(bad, good)
    text = re.sub(r"\bPRES[A-Z]*DEN\b\s*\d*-?", "", text)            # page header glued into a paragraph
    text = re.sub(r"(?<![\w(])l(\d)l(?!\w)", r"(\1)", text)          # "l2l" → "(2)"
    text = re.sub(r"\(([0-9])1(?=\s)", r"(\1)", text)
    text = re.sub(r"\((l|I)\)", "(1)", text)
    text = re.sub(r"\(l([a-z])\)", r"(1\1)", text)
    return re.sub(r"\b2O2(\d)\b", r"202\1", text)
