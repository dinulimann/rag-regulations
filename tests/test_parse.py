import pytest

from rag import consolidate, corpus, parse


@pytest.mark.parametrize("raw, want", [("2l", "21"), ("t7", "17"), ("26E}", "26B"), ("26El", "26B"), ("351", "35I"),
                                       ("7l", "71"), ("35A", "35A"), ("II", "II"), ("1O", "10"), ("abc", None)])
def test_ocr_article_numbers(raw, want):
    assert parse.norm_id(raw) == want


def test_page_furniture_is_removed():
    text = """PRESIDEN
REPUBLIK INDONESIA
-5-
SK No 187391 A
2021, No.46 -2-
6. Ketentuan . . .
Pasal 27
(1) Gubernur wajib menetapkan Upah minimum."""
    assert parse.clean_lines(text) == ["Pasal 27", "(1) Gubernur wajib menetapkan Upah minimum."]


def test_ocr_paragraph_numbers_and_words():
    assert parse.repair_ayat("(41 Selain itu (21 dan l2l, Upah Minirium") == "(4) Selain itu (2) dan (2), Upah Minimum"


def test_articles_keep_their_chapter():
    lines = ["BAB I", "KETENTUAN UMUM", "Pasal 1", "Definisi.", "BAB VI", "UPAH TERENDAH PADA USAHA MIKRO DAN USAHA",
             "KECIL", "Pasal 36", "(1) Isi.", "Pasal 37", "Isi lagi dengan rujukan", "Pasal 35H."]
    arts = parse.split_articles(lines, "x")
    assert [a.id for a in arts] == ["1", "36", "37"]                       # "Pasal 35H." is a reference, not a heading
    assert arts[1].context == ["BAB VI UPAH TERENDAH PADA USAHA MIKRO DAN USAHA KECIL"]
    assert "Pasal 35H." in arts[2].text


AMENDMENT = """PERATURAN PEMERINTAH
Pasal I
Beberapa ketentuan diubah sebagai berikut:
1. Ketentuan Pasal 2 diubah sehingga berbunyi sebagai berikut:
Pasal 2
Teks baru pasal dua.
2. Di antara Pasal 2 dan Pasal 3 disisipkan 1 (satu) pasal, yakni Pasal 2A sehingga berbunyi sebagai berikut:
Pasal 2A
Pasal sisipan.
3. Di antara BAB I dan BAB II disisipkan 1 (satu) bab, yakni BAB IA sehingga berbunyi sebagai berikut:
BAB IA
KETENTUAN LAIN
4. Di antara Pasal 3 dan Pasal 4 disisipkan 1 (satu) pasal, yakni Pasal 3A sehingga berbunyi sebagai berikut:
Pasal 3A
Di bab baru.
5. Pasal 4 dihapus.
Pasal II
Mulai berlaku.
PENJELASAN
Pasal I
Angka 1
Pasal 2
Penjelasan baru.
Pasal II
Cukup jelas."""


def test_consolidation_applies_changes_insertions_deletions_and_new_chapters():
    base = [parse.Article("x", str(i), f"Teks asli {i}.", ["BAB I UMUM"]) for i in range(1, 5)]
    cur = {a.id: a for a in consolidate.consolidate(base, {"2": "Cukup jelas."}, [("PP 9/2025", AMENDMENT)])}
    assert cur["2"].text == "Teks baru pasal dua." and cur["2"].history == ["diubah oleh PP 9/2025"]
    assert cur["2"].explanation == "Penjelasan baru."
    assert cur["2A"].history == ["disisipkan oleh PP 9/2025"] and cur["2A"].context == ["BAB I UMUM"]
    assert cur["3A"].context == ["BAB IA KETENTUAN LAIN"]                  # chapter opened by the previous item
    assert cur["4"].deleted and cur["1"].text == "Teks asli 1." and not cur["1"].history
    assert [a.id for a in consolidate.consolidate(base, {}, [("PP 9/2025", AMENDMENT)])] == ["1", "2", "2A", "3", "3A", "4"]


def test_long_articles_split_on_paragraphs_and_stay_under_the_limit():
    text = "\n".join(f"({i}) " + "kata " * 120 for i in range(1, 8))
    parts = corpus.split_long(text)
    assert len(parts) > 1 and all(len(p) <= corpus.MAX_CHARS for p in parts)
    assert all(p.startswith("(") for p in parts)


def test_flat_text_keeps_items_and_drops_running_headers():
    assert corpus.flat("(1) Upah\nadalah hak 2021, No.45\npekerja.\n(2) Lain.") == "(1) Upah adalah hak pekerja.\n(2) Lain."
