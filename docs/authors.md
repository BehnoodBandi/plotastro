# Author lists from a CSV

Assembling the author/affiliation block by hand is error-prone on long
collaborations. Feed plotastro the author CSV your collaboration already
maintains — it works with real-world lists exactly as they are:

```text
Lastname,Firstname,Authorname,Email,JoinedAsBuilder,Affiliation,ORCID,
Bandi,Behnood,Behnood Bandi, b.bandi@sussex.ac.uk, False,"Astronomy Centre, University of Sussex, Falmer, Brighton BN1 9QH, UK",0000-0001-5838-3903,
Rocher,Antoine,Antoine Rocher,antoine.rocher@epfl.ch,False,"EPFL, \'{E}cole polytechnique f\'{e}d\'{e}rale de Lausanne, Chemin des Maillettes, 51, 1290 Versoix, Switzerland",0000-0003-4349-6424,
Verdier,Aur\'{e}lien,Aur\'{e}lien Verdier,aurelien.verdier@epfl.ch,False,"EPFL, \'{E}cole polytechnique f\'{e}d\'{e}rale de Lausanne, Chemin des Maillettes, 51, 1290 Versoix, Switzerland",,
Richard,Johan,Johan Richard,johan.richard@univ-lyon1.fr,False,"CRAL, Centre de Recherche Astrophysique de Lyon, Universit\'{e} de Lyon, 9 avenue Charles Andr\'{e}, 69230 Saint-Genis-Laval, France",0000-0001-5492-1049,
Loveday,Jon ,Jon Loveday, j.loveday@sussex.ac.uk, False,"Astronomy Centre, University of Sussex, Falmer, Brighton BN1 9QH, UK",0000-0001-5290-8940,
Brown,Michael,Michael Brown,michael.brown@monash.edu,False,"Monash, School of Physics and Astronomy, Monash University, Wellington Road, Clayton, VIC 3800, Australia",0000-0002-1207-9137,
```

## What the reader understands

- **Names**: `Authorname` is preferred (alias `name`); if absent, the name
  is built from `Firstname` + `Lastname`.
- **Affiliations**: `Affiliation`/`affiliations` — several separated by
  `;`, or one row per affiliation (repeated author rows are merged).
  Numbered in order of first appearance and shared between authors
  automatically.
- **Optional**: `ORCID` (used where the format supports it) and `Email` —
  the first author with an email becomes the corresponding author.
- **Everything else is ignored** (`JoinedAsBuilder`, ...), stray spaces
  are stripped, and LaTeX already in the file (accents like `\'{e}`)
  passes through untouched.

## Generating the LaTeX

```python
import plotastro as pa
print(pa.authorlist("authors.csv", journal="mnras"))
```

```latex
\author[B. Bandi et al.]{
Behnood Bandi,$^{1}$\thanks{E-mail: b.bandi@sussex.ac.uk}
Antoine Rocher,$^{2}$
Aur\'{e}lien Verdier,$^{2}$
Johan Richard,$^{3}$
Jon Loveday$^{1}$
and Michael Brown$^{4}$
\\
% List of institutions
$^{1}$Astronomy Centre, University of Sussex, Falmer, Brighton BN1 9QH, UK\\
$^{2}$EPFL, \'{E}cole polytechnique f\'{e}d\'{e}rale de Lausanne, Chemin des Maillettes, 51, 1290 Versoix, Switzerland\\
$^{3}$CRAL, Centre de Recherche Astrophysique de Lyon, Universit\'{e} de Lyon, 9 avenue Charles Andr\'{e}, 69230 Saint-Genis-Laval, France\\
$^{4}$Monash, School of Physics and Astronomy, Monash University, Wellington Road, Clayton, VIC 3800, Australia
}
```

The same CSV works for every journal the package knows:

| `journal=` | output format |
|---|---|
| `mnras`, `rasti` | MNRAS `\author[...]{...}` block with superscripts |
| `aanda` | A&A `\inst{...}` + `\institute{...}` |
| `apj`, `oja` | AASTeX `\author[orcid]{...}` + `\affiliation`, `\correspondingauthor` |
| `prd` | REVTeX `\author` + `\email` + `\affiliation` |
| `jcap` | jcappub lettered `\affiliation[a]` + `\emailAdd` |
| `generic` | plain numbered-superscript block |

## Command line

A CLI ships with the package, so co-authors who don't use Python can run
it too:

```bash
plotastro-authors authors.csv --journal aanda
plotastro-authors authors.csv -j apj -o authors.tex
```

The output is a starting point that compiles with the journal's template —
always diff it against the class file's expectations before submission
(each output starts with a reminder comment).
