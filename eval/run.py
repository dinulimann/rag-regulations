"""Runs the labelled questions through retrieval and the answer step, and scores them.

    python -m eval.run            → eval/results.md, eval/results.json
"""

import json
import time
from pathlib import Path

import yaml

from rag import answer, store

HERE = Path(__file__).parent


def hit_facts(text: str, groups: list[list[str]]) -> bool:
    t = text.lower()
    return all(any(alt.lower() in t for alt in g) for g in groups)


def main() -> None:
    qs = yaml.safe_load((HERE / "questions.yml").read_text())
    rows = []
    for item in qs:
        r = answer.ask(item["q"])
        retrieved = {s["label"] for s in r["sources"]}
        ok_answerable = item.get("answerable", True)
        row = {"q": item["q"], "answerable": ok_answerable, "found": r["found"], "answer": r["answer"],
               "citations": r["citations"], "unsupported": r["unsupported_citations"], "seconds": r["seconds"]}
        if ok_answerable:
            exp = set(item["expect"])
            row.update(retrieved_ok=bool(exp & retrieved), cited_ok=bool(exp & set(r["citations"])),
                       facts_ok=r["found"] and hit_facts(r["answer"], item["facts"]))
        else:
            row.update(refused_ok=not r["found"])
        rows.append(row)
        mark = (f"retr {'✓' if row.get('retrieved_ok') else '✗'} cite {'✓' if row.get('cited_ok') else '✗'} "
                f"fact {'✓' if row.get('facts_ok') else '✗'}") if ok_answerable else f"refused {'✓' if row['refused_ok'] else '✗'}"
        print(f"{mark}  {r['seconds']:>5}s  {item['q'][:70]}", flush=True)
    a = [r for r in rows if r["answerable"]]
    u = [r for r in rows if not r["answerable"]]
    n = lambda key, xs: sum(1 for x in xs if x[key])  # noqa: E731
    summary = {"model": answer.MODEL, "embedding": store.EMBED_MODEL, "questions": len(rows),
               "retrieval": f"{n('retrieved_ok', a)}/{len(a)}", "cited": f"{n('cited_ok', a)}/{len(a)}",
               "facts": f"{n('facts_ok', a)}/{len(a)}", "refused_out_of_scope": f"{n('refused_ok', u)}/{len(u)}",
               "wrongly_refused": sum(1 for x in a if not x["found"]),
               "unsupported_citations": sum(len(x["unsupported"]) for x in rows),
               "avg_seconds": round(sum(x["seconds"] for x in rows) / len(rows), 1), "date": time.strftime("%Y-%m-%d")}
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=2, ensure_ascii=False))
    lines = ["# Evaluation", "", f"{summary['questions']} questions, generator `{summary['model']}`, "
             f"embeddings `{summary['embedding']}`, {summary['date']}.", "",
             f"- Right article retrieved (top 6): **{summary['retrieval']}**",
             f"- Right article cited in the answer: **{summary['cited']}**",
             f"- Key facts correct in the answer: **{summary['facts']}**",
             f"- Out-of-scope questions refused: **{summary['refused_out_of_scope']}**",
             f"- Answerable questions wrongly refused: {summary['wrongly_refused']}",
             f"- Citations to something not retrieved: {summary['unsupported_citations']}",
             f"- Average time per question: {summary['avg_seconds']} s (laptop, local model)", "",
             "| Question | Retrieved | Cited | Facts | Answer |", "|---|:-:|:-:|:-:|---|"]
    for r in rows:
        cells = ("✓" if r.get("retrieved_ok") else "✗", "✓" if r.get("cited_ok") else "✗", "✓" if r.get("facts_ok") else "✗") \
            if r["answerable"] else ("–", "–", "refused ✓" if r["refused_ok"] else "**answered ✗**")
        lines.append(f"| {r['q']} | {cells[0]} | {cells[1]} | {cells[2]} | {r['answer'][:160].replace('|', '/').replace(chr(10), ' ')} |")
    (HERE / "results.md").write_text("\n".join(lines) + "\n")
    print("\n" + "\n".join(lines[:11]))


if __name__ == "__main__":
    main()
