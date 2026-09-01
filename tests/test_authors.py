from pathlib import Path

import pytest

import plotastro as pa
from plotastro._authors import main

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "authors_example.csv"

AUTHORS = [
    {"name": "Alice Astro", "affiliations": "Uni A; Uni B",
     "orcid": "0000-0001-2345-6789", "email": "alice@uni-a.edu"},
    {"name": "Bob Bolometer", "affiliations": "Uni B", "orcid": "", "email": ""},
    {"name": "Carol Comet", "affiliations": "Uni C", "orcid": "", "email": ""},
]


def test_mnras_format():
    tex = pa.authorlist(AUTHORS, journal="mnras")
    assert "\\author[A. Astro et al.]{" in tex
    assert "Alice Astro,$^{1,2}$\\thanks{E-mail: alice@uni-a.edu}" in tex
    assert "and Carol Comet$^{3}$" in tex
    assert "$^{2}$Uni B\\\\" in tex          # shared affiliation, single entry
    assert tex.count("Uni B") == 1


def test_short_author_forms():
    one = pa.authorlist(AUTHORS[:1], journal="mnras")
    assert "\\author[A. Astro]{" in one
    two = pa.authorlist(AUTHORS[:2], journal="mnras")
    assert "\\author[Astro \\& Bolometer]{" in two


def test_aanda_format():
    tex = pa.authorlist(AUTHORS, journal="a&a")
    assert "Alice Astro\\inst{1,2}\\thanks{\\email{alice@uni-a.edu}}" in tex
    assert "\\institute{Uni A" in tex
    assert "\\and Uni C}" in tex


def test_aastex_format_apj_and_oja():
    for journal in ("apj", "oja"):
        tex = pa.authorlist(AUTHORS, journal=journal)
        assert "\\correspondingauthor{Alice Astro}" in tex
        assert "\\author[0000-0001-2345-6789]{Alice Astro}" in tex
        assert "\\author{Bob Bolometer}" in tex        # no orcid -> no [..]
        assert tex.count("\\affiliation{Uni B}") == 2  # repeated per author


def test_revtex_and_jcap_formats():
    tex = pa.authorlist(AUTHORS, journal="prd")
    assert "\\email{alice@uni-a.edu}" in tex
    tex = pa.authorlist(AUTHORS, journal="jcap")
    assert "\\author[a,b]{Alice Astro}" in tex
    assert "\\affiliation[c]{Uni C}" in tex
    assert "\\emailAdd{alice@uni-a.edu}" in tex


def test_generic_format_and_escaping():
    rows = [{"name": "A & B_Person", "affiliations": "Dept of 100% Physics"}]
    tex = pa.authorlist(rows, journal="generic")
    assert r"A \& B\_Person" in tex
    assert r"Dept of 100\% Physics" in tex


def test_existing_latex_not_double_escaped():
    rows = [{"name": r"Aur\'{e}lie Dupont",
             "affiliations": r"Universit\'{e} de Lyon \& CNRS"}]
    tex = pa.authorlist(rows, journal="generic")
    assert r"Aur\'{e}lie Dupont" in tex
    assert r"Universit\'{e} de Lyon \& CNRS" in tex   # \& kept as-is


def test_collaboration_csv_format():
    # Real-world collaboration schema: Authorname preferred, stray spaces
    # stripped, unknown columns (JoinedAsBuilder) ignored.
    rows = [
        {"Lastname": "Bandi", "Firstname": "Behnood",
         "Authorname": "Behnood Bandi", "Email": " b.bandi@sussex.ac.uk ",
         "JoinedAsBuilder": "False", "Affiliation": "Sussex",
         "ORCID": "0000-0001-5838-3903"},
        {"Lastname": "Loveday", "Firstname": "Jon ", "Authorname": "",
         "Email": "j@sussex.ac.uk", "JoinedAsBuilder": "False",
         "Affiliation": "Sussex", "ORCID": ""},
    ]
    tex = pa.authorlist(rows, journal="apj")
    assert "\\author[0000-0001-5838-3903]{Behnood Bandi}" in tex
    assert "\\email{b.bandi@sussex.ac.uk}" in tex     # spaces stripped
    assert "\\author{Jon Loveday}" in tex             # First+Last fallback
    assert "JoinedAsBuilder" not in tex


def test_duplicate_rows_merge_affiliations():
    rows = [
        {"Authorname": "Giulia Rossi", "Affiliation": "Uni A"},
        {"Authorname": "Giulia Rossi", "Affiliation": "Uni B"},
    ]
    tex = pa.authorlist(rows, journal="generic")
    assert "Giulia Rossi$^{1,2}$" in tex
    assert tex.count("Giulia Rossi") == 1


def test_only_corresponding_author_gets_thanks():
    rows = [
        {"name": "First Person", "affiliations": "A", "email": "one@x.org"},
        {"name": "Second Person", "affiliations": "A", "email": "two@x.org"},
        {"name": "Third Person", "affiliations": "A", "email": "three@x.org"},
    ]
    for journal in ("mnras", "aanda"):
        tex = pa.authorlist(rows, journal=journal)
        assert tex.count("\\thanks") == 1
        assert "one@x.org" in tex and "two@x.org" not in tex
    # jcap lists every email
    assert pa.authorlist(rows, journal="jcap").count("\\emailAdd") == 3


def test_reads_example_csv():
    tex = pa.authorlist(EXAMPLE, journal="mnras")
    # corresponding author only (everyone has an email in this list)
    assert "Behnood Bandi,$^{1}$\\thanks{E-mail: b.bandi@sussex.ac.uk}" in tex
    assert tex.count("\\thanks") == 1
    # Rocher & Verdier share EPFL (2); Bandi & Loveday share Sussex (1)
    assert "Antoine Rocher,$^{2}$" in tex
    assert r"Aur\'{e}lien Verdier,$^{2}$" in tex      # accents preserved
    assert "Jon Loveday$^{1}$" in tex                 # 'Jon ' space stripped
    assert "and Michael Brown$^{4}$" in tex
    assert "$^{4}$" in tex and "$^{5}$" not in tex    # 4 unique affiliations
    assert tex.count("University of Sussex") == 1     # shared, listed once


def test_empty_csv_raises(tmp_path):
    bad = tmp_path / "authors.csv"
    bad.write_text("name,affiliations\n")
    with pytest.raises(ValueError, match="No authors"):
        pa.authorlist(bad)


def test_cli(tmp_path, capsys):
    main([str(EXAMPLE), "-j", "aanda"])
    out = capsys.readouterr().out
    assert "\\institute{" in out
    dest = tmp_path / "authors.tex"
    main([str(EXAMPLE), "-j", "apj", "-o", str(dest)])
    assert "\\correspondingauthor" in dest.read_text()
