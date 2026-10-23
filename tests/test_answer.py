from rag import answer, store


def test_language_detection():
    assert answer.language("Berapa lama maksimal PKWT?") == "Indonesian"
    assert answer.language("How many hours of overtime are allowed?") == "English"


def test_explicit_article_references_are_recognised():
    m = list(store.REF.finditer("Apa isi Pasal 27 PP Nomor 36 Tahun 2021?"))
    assert m and m[0].group(1) == "27" and m[0].group(2) == "36" and m[0].group(3) == "2021"
    assert store.REF.search("pasal 35a")[1] == "35a"


def test_citations_must_be_retrieved(monkeypatch):
    sources = [{"id": "a", "doc": "PP 35/2021", "pasal": "8", "part": 1, "context": "BAB II", "history": [],
                "text": "PKWT paling lama 5 (lima) tahun.", "explanation": "Cukup jelas."}]
    monkeypatch.setattr(store, "search", lambda q, k=6: sources)

    class Resp:
        def raise_for_status(self): pass
        def json(self): return {"message": {"content": "Paling lama 5 tahun [1][S7] dan [PP 36/2021 Pasal 99]."}}
    monkeypatch.setattr(answer.httpx, "post", lambda *a, **k: Resp())
    r = answer.ask("Berapa lama maksimal PKWT?")
    assert r["found"] and r["citations"] == ["PP 35/2021 Pasal 8"]
    assert r["unsupported_citations"] == ["PP 36/2021 Pasal 99", "S7"]          # unknown tag and a typed label
    assert "[PP 35/2021 Pasal 8]" in r["answer"] and "[S1]" not in r["answer"]   # tags become readable labels


def test_not_found_has_no_citations(monkeypatch):
    monkeypatch.setattr(store, "search", lambda q, k=6: [])

    class Resp:
        def raise_for_status(self): pass
        def json(self): return {"message": {"content": "NOT_FOUND\nTidak ada di peraturan ini [PP 35/2021 Pasal 1]."}}
    monkeypatch.setattr(answer.httpx, "post", lambda *a, **k: Resp())
    r = answer.ask("Berapa hari cuti tahunan?")
    assert not r["found"] and r["citations"] == [] and r["answer"].startswith("Tidak ada")
