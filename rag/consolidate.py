"""Applies amending regulations to a base regulation, in order, so every answer is
based on the text in force, with the history of each article kept.

An amendment's "Pasal I" lists numbered changes. Almost every change is followed
by the complete new text of the article ("... diubah sehingga berbunyi sebagai
berikut: Pasal 27 ..."), so the new text is taken whole; deleted articles are
those named in "Pasal X dihapus." with no new text. Changed explanations are in
the amendment's own explanation part ("Angka N / Pasal X / ...").
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .parse import Article, HEAD, PASAL, clean_lines, norm_id, repair_ayat

ITEM = re.compile(r"^(\d{1,2}|l\d|\d[lI])\.?\s+(Ketentuan|Di antara|Pasal|Penjelasan|Setelah|BAB|Bab|Bagian|Lampiran)\b")


@dataclass
class Current:
    id: str
    text: str
    context: list[str]
    explanation: str = ""
    history: list[str] = field(default_factory=list)   # ["diubah oleh PP 51/2023", "disisipkan oleh PP 49/2025"]
    deleted: bool = False


def _sections(lines: list[str]) -> tuple[list[str], list[str]]:
    """(body Pasal I lines, explanation Pasal I lines) of an amendment."""
    roman = [i for i, l in enumerate(lines) if PASAL.match(l) and norm_id(PASAL.match(l).group(1)) in ("I", "II")]
    # body: first "Pasal I" .. first "Pasal II"; explanation: second "Pasal I" .. second "Pasal II"
    starts = [i for i in roman if norm_id(PASAL.match(lines[i]).group(1)) == "I"]
    stops = [i for i in roman if norm_id(PASAL.match(lines[i]).group(1)) == "II"]
    body = lines[starts[0] + 1:stops[0]]
    expl = lines[starts[1] + 1:stops[1]] if len(starts) > 1 and len(stops) > 1 else []
    return body, expl


def parse_amendment(text: str) -> tuple[dict[str, str], set[str], dict[str, str], dict[str, dict[int, str]]]:
    """(new article texts, deleted article ids, new explanations, new chapter headings per
    inserted article) from one amendment."""
    body, expl = _sections(clean_lines(text))
    new, deleted, cur, item, heads, new_heads = {}, set(), None, "", {}, {}
    item_had_article = True
    i = 0
    while i < len(body):
        line = body[i]
        h = HEAD.match(line)
        if h and i + 1 < len(body) and not ITEM.match(body[i + 1]):
            level = {"BAB": 0, "Bab": 0, "Bagian": 1, "Paragraf": 2}[h.group(1)]
            heads = {k: v for k, v in heads.items() if k < level}
            heads[level] = f"{line} {body[i + 1]}"
            i += 2
            continue
        i += 1
        if ITEM.match(line):
            # a chapter inserted by one item ("disisipkan 1 bab") holds the articles of the next
            item, cur = line, None
            if item_had_article:
                heads = {}
            item_had_article = False
            for m in re.finditer(r"Pasal\s+([0-9A-Za-z]+)\s+dihapus\.?\s*$", line):
                if norm_id(m.group(1)):
                    deleted.add(norm_id(m.group(1)))
            continue
        p = PASAL.match(line)
        pid = norm_id(p.group(1)) if p else None
        if pid and pid not in ("I", "II"):
            cur = pid
            new[cur] = ""
            item_had_article = True
            if heads:
                new_heads[cur] = dict(heads)
            continue
        if cur:
            new[cur] += ("\n" if new[cur] else "") + line
        else:
            item += " " + line                      # instruction sentence wrapped over lines
            m = re.search(r"Pasal\s+([0-9A-Za-z]+)\s+dihapus\.\s*$", item)
            if m and norm_id(m.group(1)):
                deleted.add(norm_id(m.group(1)))
    explanations, cur = {}, None
    for line in expl:
        if re.match(r"^Angka\s+\S+$", line):
            cur = None
            continue
        p = PASAL.match(line)
        pid = norm_id(p.group(1)) if p else None
        if pid and pid not in ("I", "II"):
            cur = pid
            explanations[cur] = ""
        elif cur:
            explanations[cur] += ("\n" if explanations[cur] else "") + line
    new = {k: repair_ayat(v).strip() for k, v in new.items() if v.strip()}
    return new, deleted - set(new), {k: repair_ayat(v).strip() for k, v in explanations.items()}, new_heads


def sort_key(pid: str):
    m = re.fullmatch(r"(\d+)([A-Z]?)", pid)
    return (int(m.group(1)), m.group(2)) if m else (10_000, pid)


def consolidate(base: list[Article], explanations: dict[str, str], amendments: list[tuple[str, str]]) -> list[Current]:
    """amendments: [(label, text)] in chronological order, e.g. ("PP 51/2023", text)."""
    arts = {a.id: Current(a.id, a.text.strip(), a.context, explanations.get(a.id, "")) for a in base}
    for label, text in amendments:
        new, deleted, expl, new_heads = parse_amendment(text)
        for pid, body in new.items():
            if pid in arts:
                arts[pid].text, arts[pid].deleted = body, False
                arts[pid].history.append(f"diubah oleh {label}")
            else:
                # inserted article: takes the chapter context of the article before it
                prev = max((a for a in arts.values() if sort_key(a.id) < sort_key(pid)), key=lambda a: sort_key(a.id), default=None)
                ctx = dict(enumerate(prev.context)) if prev else {}
                for level, title in new_heads.get(pid, {}).items():     # a new chapter/section opened by the amendment
                    ctx = {k: v for k, v in ctx.items() if k < level}
                    ctx[level] = repair_ayat(title)
                arts[pid] = Current(pid, body, [ctx[k] for k in sorted(ctx)], history=[f"disisipkan oleh {label}"])
        for pid in deleted:
            if pid in arts:
                arts[pid].deleted = True
                arts[pid].history.append(f"dihapus oleh {label}")
        for pid, e in expl.items():
            if pid in arts:
                arts[pid].explanation = e
    return sorted(arts.values(), key=lambda a: sort_key(a.id))
