# plotastro

[![PyPI](https://img.shields.io/pypi/v/plotastro.svg)](https://pypi.org/project/plotastro/)
[![conda-forge](https://img.shields.io/conda/vn/conda-forge/plotastro.svg)](https://anaconda.org/conda-forge/plotastro)
[![Python versions](https://img.shields.io/pypi/pyversions/plotastro.svg)](https://pypi.org/project/plotastro/)
[![CI](https://github.com/BehnoodBandi/plotastro/actions/workflows/ci.yml/badge.svg)](https://github.com/BehnoodBandi/plotastro/actions/workflows/ci.yml)
[![Docs](https://readthedocs.org/projects/plotastro/badge/?version=latest)](https://plotastro.readthedocs.io)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Publication-quality matplotlib figures for astronomy journals.**

One `pip install` gives you journal-matched styles for **MNRAS**, **RASTI**,
**A&A**, **ApJ/ApJL**, the **Open Journal of Astrophysics**, **PRD/PRL** (and
the other *Physical Review* journals), **JCAP** and **Nature Astronomy**,
as well as the chemistry journals of the **RSC** and the **ACS** — figures
at exactly the right physical size, accessible colours and colormaps from
CMasher, and helpers that make the tedious parts (sizing, panel labels,
accessibility checks, saving) one-liners.

```bash
pip install plotastro                      # or: conda install -c conda-forge plotastro
```

**Simplest usage — no new API to learn.** Importing plotastro registers the
styles with matplotlib itself; after one `plt.style.use` line you write
ordinary matplotlib, and the default figure size is already the journal's
column width:

```python
import matplotlib.pyplot as plt
import plotastro                 # just to register the styles

plt.style.use("mnras")           # or "aanda", "apj", "oja", "prd", ...
fig, ax = plt.subplots()         # plain matplotlib from here on
```

**With the helpers** (optional, but they make the tedious parts one-liners):

```python
import plotastro as pa

pa.set_style("mnras")
fig, ax = pa.subplots()          # one-column figure, golden-ratio height
ax.plot(x, y, label="model")
ax.set_xlabel("$x$")
ax.legend()
pa.savefig("myplot")             # -> myplot.pdf, ready for \includegraphics
```

| One column | Full width |
|---|---|
| ![single-column example](examples/figures/example_column.png) | ![full-width example](examples/figures/example_full.png) |

**Full documentation: [plotastro.readthedocs.io](https://plotastro.readthedocs.io)** —
or start with the [tutorial notebook](examples/tutorial.ipynb), which walks
through every feature with runnable examples.

## Why this exists

Two problems ruin most paper figures:

1. **Wrong physical size.** If you hand LaTeX a 6-inch figure and it squeezes
   it into an 84 mm column, every label shrinks by ~50 % and becomes
   unreadable. The fix: build the figure at its final printed width, then
   include it with a plain `\includegraphics{fig.pdf}` — no `[width=...]`.
2. **Inaccessible colours.** ~5 % of male readers have a colour-vision
   deficiency, and MNRAS's
   [author guidelines](https://academic.oup.com/mnras/pages/general_instructions)
   explicitly ask for colour-blind-friendly figures, and many readers print
   in greyscale. Hand-picked colour cycles, matplotlib's default among them,
   have colours that merge for these readers. Colours taken from
   [CMasher](https://cmasher.readthedocs.io)'s maps stay distinct:
   `pa.set_style("mnras", palette="cmr.rainforest")`. Then
   `pa.check_figure()` lets you verify the finished figure.

The styles share one visual language — Times-like serif fonts at ~9 pt with
~8 pt tick lettering, inward ticks on all four sides with minors, a subtle
grid, legends on a translucent white background — and differ only in figure width (plus the
sans-serif fonts Nature requires), so your plots stay **consistent between
papers** no matter where you submit. The chemistry styles (`rsc`, `acs`) keep
the ticks, grid, legends and colours but follow their publishers' rules:
sans-serif lettering, all of it at 8 pt, and no line thinner than 0.5 pt.

## Supported journals

`pa.set_style(...)`, `pa.figsize(...)` and `plt.style.use(...)` accept
(aliases in parentheses):

| key | journal | one column | full width |
|---|---|---|---|
| `mnras` | Monthly Notices of the RAS | 240.0 pt = 3.32 in | 504.0 pt = 6.97 in |
| `rasti` | RAS Techniques & Instruments | 240.0 pt = 3.32 in | 504.0 pt = 6.97 in |
| `aanda` (`a&a`, `aa`) | Astronomy & Astrophysics | 250.4 pt = 3.46 in (88 mm) | 512.2 pt = 7.09 in (180 mm) |
| `apj` (`apjl`, `aastex`) | The Astrophysical Journal | 242.3 pt = 3.35 in | 513.1 pt = 7.10 in |
| `oja` | Open Journal of Astrophysics | ≈245.3 pt = 3.39 in | ≈508 pt = 7.03 in |
| `prd` (`prl`, `revtex`) | Physical Review D, and the other *Physical Review* journals (PRL, PRA, PRB, PRC, PRE, PRX, ...), which share its REVTeX layout | 246.0 pt = 3.40 in | 510.0 pt = 7.06 in |
| `jcap` | J. Cosmology & Astroparticle Phys. | single-column ≈455 pt = 6.30 in | — |
| `natastro` (`nature`) | Nature Astronomy (sans-serif!) | 253.2 pt = 3.50 in (89 mm) | 520.7 pt = 7.20 in (183 mm) |
| `rsc` | All Royal Society of Chemistry journals (sans-serif) | 236.2 pt = 3.27 in (8.3 cm) | 486.5 pt = 6.73 in (17.1 cm) |
| `acs` (`jacs`, `achemso`) | All American Chemical Society journals (sans-serif) | 240.9 pt = 3.33 in | 505.9 pt = 7.00 in |
| `thesis` | A4 thesis text width | 426.8 pt = 5.91 in | — |
| `beamer` | Beamer slide text width | 307.3 pt = 4.25 in | — |

Widths come from each journal's LaTeX class / author guide. For a custom
document, put `\the\columnwidth` or `\the\textwidth` in your `.tex` body,
compile, read the value off the page, and pass it directly:
`pa.figsize(width=345.0)`.

### Chemistry journals (RSC and ACS)

Each chemistry publisher has one figure guide for all its journals, so
there is one style per publisher. `rsc` covers every Royal Society of
Chemistry journal (*Chemical Science*, *ChemComm*, *PCCP*, *RSC Advances*,
...), at the RSC's 8.3 cm and 17.1 cm column widths. `acs` covers every
American Chemical Society journal (*JACS*, *ACS Nano*, *Langmuir*, ...), at
3.33 in and 7 in. ACS recommends Helvetica or Arial lettering, and some
ACS journals ask for no text smaller than 8 pt, so both styles use
sans-serif fonts with all text at 8 pt. ACS also asks for no line thinner
than 0.5 pt, so the minor ticks and grid lines are 0.5 pt. RSC sets no
font rules, so `rsc` uses the same lettering as `acs`. There is no
author-list format for these journals yet (use `journal="generic"`).

The only hard dependency is matplotlib; plotastro works with both NumPy 1.x
and 2.x (CI tests each). [CMasher](https://cmasher.readthedocs.io) colours
and colormaps are an optional extra (`pip install "plotastro[cmasher]"`; see
below). Running the examples from a clone?
`pip install -r requirements-dev.txt`.

## Tutorial

### Figure sizing

```python
pa.figsize("column")                  # one column, golden-ratio height
pa.figsize("full")                    # full text width
pa.figsize("column", fraction=0.5)    # half a column
pa.figsize("column", aspect=1)        # square panel (aspect = height/width)
pa.figsize("column", journal="aanda") # size for a specific journal
pa.figsize(345.0)                     # any width in LaTeX points
```

`pa.subplots()` takes the same arguments *plus* everything `plt.subplots`
accepts, and scales the height with the grid so each panel keeps its aspect:

```python
fig, ax   = pa.subplots()                          # 1 panel, one column
fig, axes = pa.subplots(2, 2, width="full")        # 2x2 grid, full width
fig, axes = pa.subplots(1, 2, width="full", aspect=0.75, sharey=True)
```

### Colours

![CMasher colours and colormaps](examples/figures/cmasher.png)

For colours, plotastro recommends [CMasher](https://cmasher.readthedocs.io)
(van der Velden 2020, [JOSS 5, 2004](https://doi.org/10.21105/joss.02004)):
perceptually uniform scientific colormaps (sequential, diverging and
cyclic), most of them colour-vision-deficiency friendly. In its sequential
maps the lightness rises steadily from one end to the other, so colours
sampled from them stay distinct for readers with a colour-vision deficiency
*and* in greyscale print. CMasher is **not a dependency**. Install it only
if you want it (`pip install cmasher`, or `pip install "plotastro[cmasher]"`);
plotastro imports it only when you ask for a CMasher colour. Names start
with `cmr.`, as in CMasher itself:

```python
pa.set_style("mnras", palette="cmr.rainforest")    # 8-colour cycle from a CMasher map
pa.set_style("mnras", cmap="cmr.ocean")            # default colormap for imshow etc.

ax.set_prop_cycle(color=pa.cmasher_colors("torch", n=5))       # n discrete colours
ax.imshow(img, cmap=pa.cmasher_cmap("rainforest"))             # the colormap
ax.contourf(x, y, z, levels=6, cmap=pa.cmasher_cmap("iceburn", n=6))  # 6 levels
```

Discrete colours are sampled from `cmap_range=(0.15, 0.85)` by default.
This follows CMasher's advice, since most of its sequential maps run from
black to white and those ends vanish on the page. For lines that must be
easy to tell apart, CMasher suggests `apple`, `chroma`, `neon`,
`rainforest` or `torch`; for steps of one quantity, a single-hue map such
as `flamingo`, `freeze`, `gothic`, `jungle` or `ocean`. To span the whole
map with a fixed number of lines, sample exactly that many:
`pa.cmasher_colors("rainforest", n=len(models))`. Please cite CMasher if
you use it (`cmasher.get_bibtex()`).

Matched shades without transparency (better for print and EPS than `alpha=`):

```python
color = pa.cmasher_colors("torch", n=3, cmap_range=(0.3, 0.8))[0]
ax.plot(x, y, color=color)
ax.fill_between(x, lo, hi, color=pa.lighten(color, 0.6))
pa.darken(color, 0.3)     # the other direction
```

The [colours page of the documentation](https://plotastro.readthedocs.io/en/latest/colors.html)
has more: which map suits which kind of data, lines coloured by a
parameter with a colour bar, diverging and cyclic data, and common
errors. The [tutorial notebook](examples/tutorial.ipynb) runs the same
examples.

### Checking accessibility yourself

![CVD check](examples/figures/cvd_check.png)

Don't take any palette's word for it — simulate it
(Machado et al. 2009 model, no extra dependencies). The figure shows the 8
colours of `palette="cmr.rainforest"`: they stay distinct under each
simulation, because each colour is lighter than the one before.

```python
colors = pa.cmasher_colors("rainforest")
pa.check_colors(colors)           # under deuteranopia, protanopia and greyscale
pa.check_figure(fig)              # simulate a whole rendered figure — the
                                  # final check before submission
pa.simulate_cvd(colors, "deuteranopia")      # the raw transform
```

If two lines merge in any panel, add markers or dash patterns (below), or
sample fewer colours so they are further apart. MNRAS recommends
[Color Oracle](https://colororacle.org) and ColorBrewer for exactly this;
now it's built in.

### Without CMasher

Without a `palette=`, the styles use plotastro's default cycle, `pa.COLORS`
(matplotlib's `"C0"`…`"C11"`): a reordering of ColorBrewer *Set1* with
three light colours from Tableau's *Color Blind 10*. Also shipped:
`pa.OKABE_ITO` ([Okabe & Ito 2008](https://jfly.uni-koeln.de/color/)),
`pa.PETROFF10` and `pa.PETROFF8` ([Petroff 2021](https://arxiv.org/abs/2107.02270)),
`pa.TOL_VIBRANT` ([Paul Tol](https://personal.sron.nl/~pault/)) and
`pa.PAIRED` (light/dark pairs); any of them can be the cycle:
`pa.set_style("mnras", palette="okabe_ito")`. These palettes pick colours by
hue, so they are not reliably accessible: every one of them has pairs that
print as the same grey, and in the default cycle brown and red are also
hard to tell apart with protanopia. If you use them, pair the colours with
markers or dash patterns (below) and check with `pa.check_figure(fig)`.

The styles' default colormap is `viridis` (perceptually uniform, CVD-safe).
Good matplotlib picks: `viridis`/`magma`/`cividis` for sequential data,
`RdBu_r` or `coolwarm` for diverging data (red–*blue*, not red–green). Avoid
`jet`/`rainbow`. Change the default with `pa.set_style("mnras", cmap="cividis")`,
or see [cmocean](https://matplotlib.org/cmocean/).

### Markers

![markers](examples/figures/markers.png)

`pa.MARKERS = ["o", "s", "^", "D", "v", "p", "*", "X"]` — filled shapes that
survive shrinking to 4 pt. Conventions worth knowing:

| marker | typical use in astro figures |
|---|---|
| `"o"` `"s"` `"D"` | primary data series |
| `"^"` / `"v"` | **lower / upper limits** (readers expect this) |
| `"*"` `"p"` | highlight special objects (the Sun, a best-fit point) |
| `"x"` `"+"` | thin crosses — dense scatter plots, since they don't occlude |
| `"."` | huge point clouds (use `ms=1`–`2`, or better, rasterized hexbin) |

Useful tricks: `markevery=7` thins markers on dense curves;
`mfc="none"` (hollow markers) keeps overlapping datasets readable;
`ms=` and `mew=` control size and edge width.

### Line styles

![line styles](examples/figures/linestyles.png)

Beyond matplotlib's `"-"`, `"--"`, `":"`, `"-."`, the dict `pa.LINESTYLES`
provides named dash tuples of the form `(offset, (on, off, ...))` in points:

```python
ax.plot(x, y, ls=pa.LINESTYLES["long dash"])       # (0, (9, 3))
ax.plot(x, y, ls=(0, (4, 1, 1, 1)))                # or roll your own
```

Guidelines: keep to ≤ 4 distinct dash patterns per panel (more becomes
noise); use solid for data / the headline result and dashes/dots for models
and references; MNRAS explicitly warns against triple-dot-dashed lines.

### Redundant encoding — the cycler

Colour should never be the *only* difference between curves. `pa.style_cycler`
advances colour, marker and/or line style **in step**, so every series is
unique in two or three channels at once (and survives greyscale printing):

![redundant encoding](examples/figures/redundant_encoding.png)

```python
ax.set_prop_cycle(pa.style_cycler(markers=True))              # one axes
ax.set_prop_cycle(pa.style_cycler(linestyles=True, markers=True))
plt.rc("axes", prop_cycle=pa.style_cycler(markers=True))      # everywhere
```

### Panel labels

Journals want multi-panel figures labelled (a), (b), (c)…:

```python
fig, axes = pa.subplots(2, 2, width="full")
pa.label_panels(axes)                                    # (a) (b) (c) (d)
pa.label_panels(axes, loc="outside", fmt="{}", fontweight="bold")  # Nature style
pa.label_panels(axes, uppercase=True, loc="lower right") # (A) ... bottom-right
```

### LaTeX text rendering

By default the styles use matplotlib **mathtext** with STIX fonts:
Times-compatible maths, zero dependencies. For pixel-perfect agreement with
your manuscript (custom macros, real kerning):

```python
pa.set_style("mnras", usetex=True)   # needs latex + dvipng + ghostscript
```

This loads the `newtx` Times fonts (matching the MNRAS/A&A house font), or
Helvetica for Nature Astronomy and the chemistry styles. Develop with `usetex=False`, flip it on for the
final version — LaTeX rendering is slow.

### Saving figures

The styles bake in submission-friendly defaults: **PDF** output, 450 dpi for
rasterised elements (journals want ≥ 300–400), tight bounding box, and
TrueType font embedding (`pdf.fonttype: 42`, so no Type-3 font rejections).

```python
pa.savefig("figure1")                              # figure1.pdf
pa.savefig("figure1", formats=("pdf", "png"))      # + a PNG for slides/Slack
pa.savefig("figure1", fig=fig, dpi=600)            # extra options pass through
```

If a journal insists on EPS, note EPS has **no transparency** — replace
`alpha=` with `pa.lighten()` shades (a good habit anyway).

### Author lists from a CSV

Assembling the author/affiliation block by hand is error-prone on long
collaborations. Feed plotastro the author CSV your collaboration already
maintains — it works with real-world lists exactly as they are
(this is [examples/authors_example.csv](examples/authors_example.csv)):

```csv
Lastname,Firstname,Authorname,Email,JoinedAsBuilder,Affiliation,ORCID,
Bandi,Behnood,Behnood Bandi, b.bandi@sussex.ac.uk, False,"Astronomy Centre, University of Sussex, Falmer, Brighton BN1 9QH, UK",0000-0001-5838-3903,
Rocher,Antoine,Antoine Rocher,antoine.rocher@epfl.ch,False,"EPFL, \'{E}cole polytechnique f\'{e}d\'{e}rale de Lausanne, Chemin des Maillettes, 51, 1290 Versoix, Switzerland",0000-0003-4349-6424,
Verdier,Aur\'{e}lien,Aur\'{e}lien Verdier,aurelien.verdier@epfl.ch,False,"EPFL, \'{E}cole polytechnique f\'{e}d\'{e}rale de Lausanne, Chemin des Maillettes, 51, 1290 Versoix, Switzerland",,
Richard,Johan,Johan Richard,johan.richard@univ-lyon1.fr,False,"CRAL, Centre de Recherche Astrophysique de Lyon, Universit\'{e} de Lyon, 9 avenue Charles Andr\'{e}, 69230 Saint-Genis-Laval, France",0000-0001-5492-1049,
Loveday,Jon ,Jon Loveday, j.loveday@sussex.ac.uk, False,"Astronomy Centre, University of Sussex, Falmer, Brighton BN1 9QH, UK",0000-0001-5290-8940,
Brown,Michael,Michael Brown,michael.brown@monash.edu,False,"Monash, School of Physics and Astronomy, Monash University, Wellington Road, Clayton, VIC 3800, Australia",0000-0002-1207-9137,
```

It recognises `Authorname` (or `name`, or `Firstname`+`Lastname`),
`Affiliation`/`affiliations` (several separated by `;`, or one row per
affiliation — repeated author rows are merged), and optional `ORCID` and
`Email`; **every other column is ignored** (`JoinedAsBuilder`, ...), stray
spaces are stripped, and LaTeX already in the file (accents like `\'{e}`)
passes through untouched. Affiliations are numbered in order of first
appearance and shared between authors automatically; the first author with
an email becomes the corresponding author.

```python
print(pa.authorlist("authors_example.csv", journal="mnras"))
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

The same CSV works for every astronomy and physics journal: `mnras`/`rasti`,
`aanda` (`\inst`/`\institute`), `apj`/`oja` (AASTeX `\author`/`\affiliation`
with ORCIDs), `prd` (REVTeX), `jcap` (lettered `\affiliation[a]`), or
`generic` for a plain numbered block (the chemistry journals have no
format of their own yet). A command-line tool ships with the package, so
co-authors who don't use Python can run it too:

```bash
plotastro-authors authors.csv --journal aanda
plotastro-authors authors.csv -j apj -o authors.tex
```

See [examples/authors_example.csv](examples/authors_example.csv) for a
complete example.

## API summary

| | |
|---|---|
| `set_style(journal, usetex=, grid=, palette=, cmap=, **rc)` | activate a journal's style (alias: `use`) |
| `authorlist(csv, journal=)` | LaTeX author/affiliation block from a CSV (CLI: `plotastro-authors`) |
| `figsize(width, journal=, fraction=, aspect=, ...)` | journal-correct figure dimensions |
| `subplots(...)` | `plt.subplots` with the size computed for you |
| `savefig(name, formats=("pdf",))` | save one figure in several formats |
| `label_panels(axes, ...)` | (a), (b), (c) panel labels |
| `style_cycler(markers=, linestyles=)` | redundant-encoding property cycle |
| `cmasher_colors(cmap, n=, cmap_range=)`, `cmasher_cmap(cmap, cmap_range=, n=)` | CMasher colours / colormaps (optional `cmasher` package) |
| `COLORS`, `CYCLE`, `OKABE_ITO`, `PETROFF8`, `PETROFF10`, `TOL_VIBRANT`, `PAIRED` | built-in palettes |
| `lighten(c, f)`, `darken(c, f)` | matched shades without transparency |
| `simulate_cvd`, `check_colors`, `check_figure` | colour-vision-deficiency checks |
| `MARKERS`, `LINESTYLES` | curated marker / dash-pattern sequences |
| `show_colors()`, `show_markers()`, `show_linestyles()` | reference charts |
| `current_journal()`, `JOURNALS`, `GOLDEN` | introspection |
| `set_size(...)` | deprecated alias for the original `myfigsize` API |

## Tweaks and FAQ

- **Turn the grid off:** `pa.set_style("mnras", grid=False)`, or per-axes
  `ax.grid(False)`.
- **Override anything:** `pa.set_style("mnras", **{"font.size": 10})`, or
  `plt.rcParams[...] = ...` after `set_style`.
- **"Times New Roman not found" warning:** the font list falls back through
  Times → Nimbus Roman → STIX → DejaVu automatically; install
  `mscorefonts`/STIX to silence it, or ignore it.
- **Labels getting cut off?** They shouldn't be — the styles enable
  `constrained_layout`. If you manage layout manually, disable it with
  `plt.rcParams["figure.constrained_layout.use"] = False`.
- **Astronomical images:** use `origin="lower"` in `imshow` (or uncomment
  `image.origin: lower` in the style file), and `ax.grid(False)`.
- **Figures look huge/small on screen:** that's just `figure.dpi: 150` for
  display; the saved size is exact.
- **Styles without Python helpers:** after `import plotastro` once,
  `plt.style.use("mnras")` works in any code; or copy the `.mplstyle` files
  from `src/plotastro/styles/` into `matplotlib.get_configdir()/stylelib/`.
- **Old API:** `plotastro.set_size(...)` reproduces the original
  `myfigsize.set_size()`; the old `MNRAS_Style.mplstyle` is now
  `plt.style.use("mnras")`.

## Development

```bash
git clone <this repo> && cd <repo>
pip install -e ".[dev]"
pytest                              # run the test suite
python tools/generate_styles.py     # regenerate styles/ after editing the template
python examples/make_reference_figures.py   # regenerate README figures
```

The `.mplstyle` files are generated from the templates in
[tools/generate_styles.py](tools/generate_styles.py) — edit that, not the
files (CI checks they stay in sync). Releases: bump the version in
`pyproject.toml` and `CHANGELOG.md`, then push a `v*` tag — the
[publish workflow](.github/workflows/publish.yml) builds and uploads to PyPI
(see the one-time trusted-publishing setup notes in that file).

## Credits

- Original MNRAS style this grew from:
  [M. Knabenhans' mplstyle_for_MNRAS](https://github.com/miknab/mplstyle_for_MNRAS)
- Set1 ordering of the default cycle:
  [Thøger Rivera-Thorsen](https://gist.github.com/thriveth/8560036);
  light colours from Tableau *Color Blind 10*
- Palettes: [Okabe & Ito](https://jfly.uni-koeln.de/color/),
  [Petroff (2021)](https://arxiv.org/abs/2107.02270),
  [Paul Tol](https://personal.sron.nl/~pault/), ColorBrewer *Paired*
- Optional colormaps: [CMasher](https://cmasher.readthedocs.io)
  (E. van der Velden 2020, JOSS 5, 2004; BSD-3-Clause), used as an optional
  dependency, not bundled
- CVD model: Machado, Oliveira & Fernandes (2009), IEEE TVCG 15(6)
- Figure-size approach after
  [Jack Walton's guide](https://jwalton.info/Embed-Publication-Matplotlib-Latex/)
- Journal guidelines:
  [MNRAS](https://academic.oup.com/mnras/pages/general_instructions) ·
  [A&A](https://www.aanda.org/for-authors) ·
  [AAS Journals](https://journals.aas.org/graphics-guide/) ·
  [OJA](https://astro.theoj.org/site/instructions) ·
  [APS](https://journals.aps.org/authors) ·
  [Nature](https://www.nature.com/nature/for-authors/formatting-guide) ·
  [RSC](https://www.rsc.org/journals-books-databases/author-and-reviewer-hub/authors-information/prepare-and-format/figures-graphics-images/) ·
  [ACS](https://researcher-resources.acs.org/publish/author_guidelines?coden=jacsat)

MIT licensed — see [LICENSE](LICENSE).
