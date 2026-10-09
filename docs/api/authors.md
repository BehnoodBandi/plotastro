# Author lists

Journal-ready LaTeX author and affiliation blocks from your
collaboration's CSV file. See {doc}`../authors` for the CSV format and
example output.

```{eval-rst}
.. currentmodule:: plotastro

.. autofunction:: authorlist
```

## Output formats

| `journal=` | format |
|---|---|
| `mnras`, `rasti` | MNRAS `\author[...]{...}` block with superscripts and a `\thanks` e-mail |
| `aanda`, `euclid` | A&A `\inst{...}` and `\institute{...}` (`euclid` for the `aaEC` class) |
| `apj`, `oja` | AASTeX `\author[orcid]{...}`, `\affiliation`, `\correspondingauthor` |
| `prd` | REVTeX `\author`, `\email`, `\affiliation` |
| `jcap` | jcappub lettered `\affiliation[a]` and `\emailAdd` |
| `generic`, `natastro`, `thesis`, `beamer` | a plain block with numbered superscripts |

Journal aliases work here too (see {ref}`api-journal-names`). The
chemistry styles `rsc` and `acs` have no format yet: asking for one raises
a `ValueError`, so use `generic` for those papers.

## Command line

Installing plotastro also installs `plotastro-authors`, which wraps
{func}`authorlist`:

```text
usage: plotastro-authors [-h] [-j JOURNAL] [-o OUTPUT] csv

positional arguments:
  csv                   path to the author CSV file

options:
  -h, --help            show this help message and exit
  -j JOURNAL, --journal JOURNAL
                        journal key, e.g. mnras, aanda, apj, oja, prd, jcap,
                        or 'generic' (default: mnras)
  -o OUTPUT, --output OUTPUT
                        write to this .tex file instead of stdout
```

For example, `plotastro-authors authors.csv -j apj -o authors.tex`. On an
error (a missing file, or a CSV without names) it prints the message and
exits with status 1.
