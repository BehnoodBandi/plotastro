"""Generate journal-ready LaTeX author/affiliation blocks from a CSV file.

Works directly with real collaboration author lists. Recognised columns
(header names are case-insensitive; **any other column is ignored**, so
collaboration bookkeeping like ``JoinedAsBuilder`` is fine):

    Authorname     display name, e.g. "Behnood Bandi" (alias: "name");
                   if absent, built from "Firstname" + "Lastname"
    Affiliation    one or more affiliations separated by ";"
                   (aliases: "affiliations", "affil", "affiliation1", ...)
    ORCID          optional
    Email          optional; authors with an email are marked corresponding

Example (a typical collaboration list)::

    Lastname,Firstname,Authorname,Email,JoinedAsBuilder,Affiliation,ORCID,
    Bandi,Behnood,Behnood Bandi, b.bandi@sussex.ac.uk, False,"Astronomy Centre, University of Sussex, Falmer, Brighton BN1 9QH, UK",0000-0001-5838-3903,
    Dupont,Aur\\'{e}lie,Aur\\'{e}lie Dupont,,False,"CRAL, Universit\\'{e} de Lyon, France",0000-0002-1825-0097,

Notes:

- LaTeX already present in the CSV (accents like ``\\'{e}``, maths, ...)
  is passed through untouched; only unescaped ``& % # _`` are escaped.
- Whitespace around values is stripped (`` b.bandi@...`` is fine).
- An author appearing on **several rows** (one per affiliation, as some
  collaborations do) is merged into one entry with all affiliations.
- Author order = row order; affiliations are numbered in order of first
  appearance and shared between authors automatically.

Usage from Python::

    import plotastro as pa
    print(pa.authorlist("authors.csv", journal="mnras"))

or from the command line (installed with the package)::

    plotastro-authors authors.csv --journal mnras
    plotastro-authors authors.csv -j apj -o authors.tex

The output is a starting point that compiles with the journal's template —
fine-tune addresses, footnotes etc. in the .tex file.
"""

from __future__ import annotations

import argparse
import csv
import re
import string
from pathlib import Path

# Journals sharing an author-block format:
_FORMATS = {
    "mnras": "mnras", "rasti": "mnras",
    "aanda": "aanda",
    "apj": "aastex", "oja": "aastex",
    "prd": "revtex",
    "jcap": "jcap",
    "generic": "generic", "natastro": "generic",
    "thesis": "generic", "beamer": "generic",
}

def _escape(text):
    """Escape unescaped & % # _ for LaTeX; leave existing LaTeX alone."""
    return re.sub(r"(?<!\\)([&%#_])", r"\\\1", str(text).strip())


def _norm_key(key):
    return str(key).strip().lower().replace(" ", "").replace("_", "")


def _read_authors(source):
    """Return a list of {name, affils, orcid, email} dicts.

    `source` is a CSV path, or an already-parsed list of dicts (with the
    same keys as the CSV columns) for programmatic use. See the module
    docstring for the recognised columns; rows repeating an author's name
    are merged (extra affiliations appended).
    """
    if isinstance(source, (str, Path)):
        with open(source, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
    else:
        rows = [dict(row) for row in source]

    authors, seen = [], {}
    for raw in rows:
        row = {_norm_key(k): (v or "").strip() for k, v in raw.items() if k}
        name = (row.get("authorname") or row.get("name") or " ".join(
            part for part in (row.get("firstname"), row.get("lastname")) if part))
        if not name:
            continue
        affils = []
        for key in sorted(row):  # affiliation, affiliations, affiliation1, ...
            if key.startswith("affil"):
                affils += [a.strip() for a in row[key].split(";") if a.strip()]

        author = seen.get(name.lower())
        if author is None:
            author = {"name": _escape(name), "affils": [],
                      "orcid": "", "email": ""}
            seen[name.lower()] = author
            authors.append(author)
        for aff in affils:
            escaped = _escape(aff)
            if escaped not in author["affils"]:
                author["affils"].append(escaped)
        author["orcid"] = author["orcid"] or row.get("orcid", "")
        author["email"] = author["email"] or row.get("email", "")
    if not authors:
        raise ValueError(
            "No authors found — the CSV needs an 'Authorname' or 'name' "
            "column (or 'Firstname'/'Lastname') with at least one "
            "non-empty row.")
    return authors


def _affiliation_index(authors):
    """Ordered unique affiliations -> 1-based numbering."""
    index = {}
    for a in authors:
        for aff in a["affils"]:
            index.setdefault(aff, len(index) + 1)
    return index


def _short_authors(authors):
    """Running-head form: 'B. Bandi et al.', 'Doe & Roe', or 'B. Bandi'."""
    def surname(a):
        return a["name"].split()[-1]

    first = authors[0]["name"].split()
    initial = f"{first[0][0]}. {first[-1]}" if len(first) > 1 else first[0]
    if len(authors) == 1:
        return initial
    if len(authors) == 2:
        return f"{surname(authors[0])} \\& {surname(authors[1])}"
    return f"{initial} et al."


def _sup(author, index):
    nums = ",".join(str(n) for n in sorted(index[a] for a in author["affils"]))
    return f"$^{{{nums}}}$" if nums else ""


def _corresponding(authors):
    """First author with an email — the only one footnoted in the
    single-\\thanks formats (MNRAS, A&A)."""
    return next((a for a in authors if a["email"]), None)


def _fmt_mnras(authors, index):
    corr = _corresponding(authors)
    lines = [f"\\author[{_short_authors(authors)}]{{"]
    for i, a in enumerate(authors):
        thanks = f"\\thanks{{E-mail: {a['email']}}}" if a is corr else ""
        if len(authors) > 1 and i == len(authors) - 1:
            lines.append(f"and {a['name']}{_sup(a, index)}{thanks}")
        elif i >= len(authors) - 2:  # no comma before the final 'and'
            lines.append(f"{a['name']}{_sup(a, index)}{thanks}")
        else:
            lines.append(f"{a['name']},{_sup(a, index)}{thanks}")
    lines += ["\\\\", "% List of institutions"]
    insts = [f"$^{{{n}}}$" + aff for aff, n in index.items()]
    lines.append("\\\\\n".join(insts))
    lines.append("}")
    return "\n".join(lines)


def _fmt_aanda(authors, index):
    corr = _corresponding(authors)
    parts = []
    for a in authors:
        nums = ",".join(str(n) for n in sorted(index[x] for x in a["affils"]))
        inst = f"\\inst{{{nums}}}" if nums else ""
        thanks = f"\\thanks{{\\email{{{a['email']}}}}}" if a is corr else ""
        parts.append(f"{a['name']}{inst}{thanks}")
    author_block = "\\author{" + "\n        \\and ".join(parts) + "}"
    inst_block = ("\\institute{" +
                  "\n           \\and ".join(index) + "}")
    return author_block + "\n\n" + inst_block


def _fmt_aastex(authors, index):
    blocks = []
    corresponding = _corresponding(authors)
    if corresponding:
        blocks.append(f"\\correspondingauthor{{{corresponding['name']}}}\n"
                      f"\\email{{{corresponding['email']}}}")
    for a in authors:
        opt = f"[{a['orcid']}]" if a["orcid"] else ""
        lines = [f"\\author{opt}{{{a['name']}}}"]
        lines += [f"\\affiliation{{{aff}}}" for aff in a["affils"]]
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def _fmt_revtex(authors, index):
    blocks = []
    for a in authors:
        lines = [f"\\author{{{a['name']}}}"]
        if a["email"]:
            lines.append(f"\\email{{{a['email']}}}")
        lines += [f"\\affiliation{{{aff}}}" for aff in a["affils"]]
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def _fmt_jcap(authors, index):
    # jcappub labels affiliations with letters
    if len(index) > 26:
        raise ValueError("The JCAP format supports at most 26 affiliations.")
    letters = {aff: string.ascii_lowercase[n - 1] for aff, n in index.items()}
    lines = []
    for a in authors:
        labels = ",".join(sorted(letters[x] for x in a["affils"]))
        opt = f"[{labels}]" if labels else ""
        lines.append(f"\\author{opt}{{{a['name']}}}")
    lines.append("")
    lines += [f"\\affiliation[{letters[aff]}]{{{aff}}}" for aff in index]
    emails = [a["email"] for a in authors if a["email"]]
    if emails:
        lines.append("")
        lines += [f"\\emailAdd{{{e}}}" for e in emails]
    return "\n".join(lines)


def _fmt_generic(authors, index):
    names = [f"{a['name']}{_sup(a, index)}" for a in authors]
    if len(names) > 1:
        head = ", ".join(names[:-1]) + " and " + names[-1]
    else:
        head = names[0]
    insts = [f"$^{{{n}}}$" + aff for aff, n in index.items()]
    return head + "\n\n" + "\n".join(insts)


_RENDERERS = {"mnras": _fmt_mnras, "aanda": _fmt_aanda, "aastex": _fmt_aastex,
              "revtex": _fmt_revtex, "jcap": _fmt_jcap, "generic": _fmt_generic}


def authorlist(source, journal="mnras"):
    """LaTeX author/affiliation block for a journal, from a CSV file.

    Parameters
    ----------
    source : str, Path, or list of dicts
        Path to a CSV file with columns ``name``, ``affiliations``
        (";"-separated), ``orcid``, ``email`` — or an equivalent list of
        dicts. See the module docstring for the format.
    journal : str
        Any journal key/alias the package knows (``"mnras"``, ``"aanda"``,
        ``"apj"``, ``"oja"``, ``"prd"``, ``"jcap"``, ...) or ``"generic"``
        for a plain numbered-superscript block.

    Returns
    -------
    str : LaTeX source to paste into your manuscript.

    Examples
    --------
    >>> print(pa.authorlist("authors.csv", journal="aanda"))
    """
    from ._core import _resolve
    key = "generic" if str(journal).lower() == "generic" else _resolve(journal)
    fmt = _FORMATS[key]
    authors = _read_authors(source)
    index = _affiliation_index(authors)
    header = (f"% Author list generated by plotastro ({key} format)\n"
              f"% Check addresses/footnotes against the journal template.\n")
    return header + _RENDERERS[fmt](authors, index)


def main(argv=None):
    """Command-line entry point: ``plotastro-authors authors.csv -j mnras``."""
    parser = argparse.ArgumentParser(
        prog="plotastro-authors",
        description="Generate a journal-ready LaTeX author/affiliation block "
                    "from a CSV file (columns: Authorname or Firstname/"
                    "Lastname, Affiliation, ORCID, Email; extra columns are "
                    "ignored).")
    parser.add_argument("csv", help="path to the author CSV file")
    parser.add_argument("-j", "--journal", default="mnras",
                        help="journal key, e.g. mnras, aanda, apj, oja, prd, "
                             "jcap, or 'generic' (default: mnras)")
    parser.add_argument("-o", "--output",
                        help="write to this .tex file instead of stdout")
    args = parser.parse_args(argv)
    try:
        tex = authorlist(args.csv, journal=args.journal)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"error: {exc}\n")
    if args.output:
        Path(args.output).write_text(tex + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(tex)


if __name__ == "__main__":
    main()
