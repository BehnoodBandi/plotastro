# Publication-quality matplotlib styles for astronomy journals

Matplotlib styles and helper functions that produce figures which drop straight
into **MNRAS**, **A&A**, **ApJ/ApJL** and **Open Journal of Astrophysics**
papers at exactly the right size — with a consistent, colour-blind-friendly
look across all of them.

```python
import matplotlib.pyplot as plt
import paperplot as pp

pp.set_style("mnras")            # or "aanda", "apj", "oja"
fig, ax = pp.subplots()          # one-column figure, golden-ratio height
ax.plot(x, y, label="model")
ax.set_xlabel("$x$")
ax.legend()
pp.savefig("myplot")             # -> myplot.pdf, ready for \includegraphics
```

| One column | Full width |
|---|---|
| ![single-column example](examples/figures/example_column.png) | ![full-width example](examples/figures/example_full.png) |

**Start with the [tutorial notebook](examples/tutorial.ipynb)** — it walks
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
   explicitly ask for colour-blind-friendly figures. The default matplotlib
   cycle is not; the one here is.

This toolkit fixes both, once, for all your papers.

## Contents

```
styles/mnras.mplstyle    Monthly Notices of the RAS
styles/aanda.mplstyle    Astronomy & Astrophysics
styles/apj.mplstyle      The Astrophysical Journal (AASTeX)
styles/oja.mplstyle      The Open Journal of Astrophysics
paperplot.py             helper module (sizing, colours, cyclers, saving)
examples/tutorial.ipynb  hands-on tutorial (executed, plots included)
examples/make_reference_figures.py  regenerates the images in this README
myfigsize.py             deprecated shim for the old set_size() API
```

The four styles share one visual language — Times-like serif fonts, 9 pt text
with ~8 pt tick lettering, inward ticks on all four sides with minors, a
subtle grid, frameless legends, and the colour-blind-friendly cycle. Only the
default figure width differs, so plots stay **consistent between your papers**
no matter where you submit.

## Installation

No packaging, by design — copy what you need:

- **Per project (recommended):** copy `paperplot.py` and the `styles/` folder
  next to your analysis scripts (or clone the repo and add it to your
  `PYTHONPATH`). `paperplot` finds the styles relative to its own location.
- **Styles only, available everywhere:** copy the `.mplstyle` files into
  `matplotlib.get_configdir() + "/stylelib/"` (usually `~/.config/matplotlib/stylelib/`
  or `~/.matplotlib/stylelib/`). Then `plt.style.use("mnras")` works in any
  script without this repo.

Requires only `matplotlib` (any recent version; no LaTeX needed by default).

## Supported journals and figure widths

`pp.set_style(...)` and `pp.figsize(...)` accept these names (aliases in
parentheses):

| key | journal | one column | full width |
|---|---|---|---|
| `mnras` | Monthly Notices of the RAS | 240.0 pt = 3.32 in | 504.0 pt = 6.97 in |
| `aanda` (`a&a`, `aa`) | Astronomy & Astrophysics | 250.4 pt = 3.46 in (88 mm) | 512.2 pt = 7.09 in (180 mm) |
| `apj` (`apjl`, `aastex`) | The Astrophysical Journal | 242.3 pt = 3.35 in | 513.1 pt = 7.10 in |
| `oja` | Open Journal of Astrophysics | ≈245.3 pt = 3.39 in | ≈508 pt = 7.03 in |
| `thesis` | A4 thesis text width | 426.8 pt = 5.91 in | — |
| `beamer` | Beamer slide text width | 307.3 pt = 4.25 in | — |

Widths come from each journal's LaTeX class / author guide. To measure your
own document (custom class, thesis template, ...), put `\the\columnwidth` or
`\the\textwidth` anywhere in the `.tex` body, compile, and read the value off
the page or the `.log`; then pass it directly: `pp.figsize(width=345.0)`.

## Tutorial

### Figure sizing

```python
pp.figsize("column")                  # one column, golden-ratio height
pp.figsize("full")                    # full text width
pp.figsize("column", fraction=0.5)    # half a column
pp.figsize("column", aspect=1)        # square panel (aspect = height/width)
pp.figsize("column", journal="aanda") # size for a specific journal
pp.figsize(345.0)                     # any width in LaTeX points
```

`pp.subplots()` takes the same arguments *plus* everything `plt.subplots`
accepts, and scales the height with the grid so each panel keeps its aspect:

```python
fig, ax   = pp.subplots()                          # 1 panel, one column
fig, axes = pp.subplots(2, 2, width="full")        # 2x2 grid, full width
fig, axes = pp.subplots(1, 2, width="full", aspect=0.75, sharey=True)
```

### The colour palette

![default palette](examples/figures/palette.png)

The default cycle has 12 colours, all accessible by name via `pp.COLORS`
(e.g. `pp.COLORS["blue"]`), or as matplotlib's `"C0"`…`"C11"` shorthands:

- **C0–C8** are a colour-blind-safe re-ordering of the
  [ColorBrewer](https://colorbrewer2.org) *Set1* qualitative palette
  (popularised by [Thøger Rivera-Thorsen's CBcycle](https://gist.github.com/thriveth/8560036)).
  Consecutive colours differ in **lightness as well as hue**, so adjacent
  lines stay distinguishable under the common deficiencies (deuteranopia,
  protanopia) *and* in greyscale print; the notorious red–green pair is
  pushed far apart in the cycle (green is C2, red is C7), so plots with a
  handful of lines never rely on it.
- **C9–C11** are light companions (from Tableau's *Color Blind 10*): use them
  for uncertainty bands, reference curves, or de-emphasised data underneath a
  saturated line of the same hue.

Matched shades without transparency (better for print and EPS):

```python
ax.plot(x, y, color=pp.COLORS["blue"])
ax.fill_between(x, lo, hi, color=pp.lighten(pp.COLORS["blue"], 0.7))
pp.darken(pp.COLORS["orange"], 0.3)     # the other direction
```

Also included: `pp.OKABE_ITO`, the [Okabe & Ito (2008)](https://jfly.uni-koeln.de/color/)
8-colour palette — the classic recommendation for categorical colours in
science. Check any figure yourself with
[Color Oracle](https://colororacle.org) (simulates CVD on screen) or the
[Coblis simulator](https://www.color-blindness.com/coblis-color-blindness-simulator/) —
MNRAS recommends exactly these tools.

**Colormaps:** the styles default to `viridis` (perceptually uniform,
CVD-safe). Good picks: `viridis`/`magma`/`cividis` for sequential data,
`RdBu_r` or `coolwarm` for diverging data (red–*blue*, not red–green). Avoid
`jet`/`rainbow`. For more astro-friendly maps see
[cmasher](https://cmasher.readthedocs.io) and [cmocean](https://matplotlib.org/cmocean/).

### Markers

![markers](examples/figures/markers.png)

`pp.MARKERS = ["o", "s", "^", "D", "v", "p", "*", "X"]` — filled shapes that
survive shrinking to 4 pt. Conventions worth knowing:

| marker | typical use in astro figures |
|---|---|
| `"o"` `"s"` `"D"` | primary data series |
| `"^"` / `"v"` | **lower / upper limits** (readers expect this) |
| `"*"` `"p"` | highlight special objects (the Sun, a best-fit point) |
| `"x"` `"+"` | thin crosses — dense scatter plots, since they don't occlude |
| `"."` | huge point clouds (use `ms=1`–`2`, or better, `alpha` + rasterized) |

Useful tricks: `markevery=7` thins markers on dense curves;
`mfc="none"` (hollow markers) keeps overlapping datasets readable;
`ms=` and `mew=` control size and edge width.

### Line styles

![line styles](examples/figures/linestyles.png)

Beyond matplotlib's `"-"`, `"--"`, `":"`, `"-."`, the dict `pp.LINESTYLES`
provides named dash tuples of the form `(offset, (on, off, ...))` in points:

```python
ax.plot(x, y, ls=pp.LINESTYLES["long dash"])       # (0, (9, 3))
ax.plot(x, y, ls=(0, (4, 1, 1, 1)))                # or roll your own
```

Guidelines: keep to ≤ 4 distinct dash patterns per panel (more becomes
noise); use solid for data / the headline result and dashes/dots for models
and references; MNRAS explicitly warns against triple-dot-dashed lines.

### Redundant encoding — the cycler

Colour should never be the *only* difference between curves. `pp.style_cycler`
advances colour, marker and/or line style **in step**, so every series is
unique in two or three channels at once (and survives greyscale printing):

![redundant encoding](examples/figures/redundant_encoding.png)

```python
ax.set_prop_cycle(pp.style_cycler(markers=True))              # one axes
ax.set_prop_cycle(pp.style_cycler(linestyles=True, markers=True))
plt.rc("axes", prop_cycle=pp.style_cycler(markers=True))      # everywhere
```

### LaTeX text rendering

By default the styles use matplotlib **mathtext** with STIX fonts:
Times-compatible maths, zero dependencies. For pixel-perfect agreement with
your manuscript (custom macros, real kerning):

```python
pp.set_style("mnras", usetex=True)   # needs latex + dvipng + ghostscript
```

This loads the `newtx` Times fonts, matching the MNRAS/A&A house font.
Develop with `usetex=False`, flip it on for the final version — LaTeX
rendering is slow.

### Saving figures

The styles bake in submission-friendly defaults: **PDF** output, 450 dpi for
rasterised elements (journals want ≥ 300–400), tight bounding box, and
TrueType font embedding (`pdf.fonttype: 42`, so no Type-3 font rejections).

```python
pp.savefig("figure1")                              # figure1.pdf
pp.savefig("figure1", formats=("pdf", "png"))      # + a PNG for slides/Slack
pp.savefig("figure1", fig=fig, dpi=600)            # extra options pass through
```

If a journal insists on EPS, note EPS has **no transparency** — replace
`alpha=` with `pp.lighten()` shades (a good habit anyway).

## Tweaks and FAQ

- **Turn the grid off:** `pp.set_style("mnras", grid=False)`, or per-axes
  `ax.grid(False)`, or edit `axes.grid` in the style file.
- **Override anything:** `pp.set_style("mnras", **{"font.size": 10})`, or
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
- **Old API:** `myfigsize.set_size(...)` still works (it now forwards to
  `pp.figsize`); the old `MNRAS_Style.mplstyle` became `styles/mnras.mplstyle`.

## Credits

- Original MNRAS style: [M. Knabenhans' mplstyle_for_MNRAS](https://github.com/mischakn/mplstyle_for_MNRAS) (basis of this repo)
- Colour-blind-friendly Set1 ordering: [Thøger Rivera-Thorsen](https://gist.github.com/thriveth/8560036); light colours from Tableau *Color Blind 10*
- Okabe & Ito palette: [Color Universal Design](https://jfly.uni-koeln.de/color/)
- Figure-size approach after [Jack Walton's guide](https://jwalton.info/Embed-Publication-Matplotlib-Latex/)
- Journal guidelines: [MNRAS](https://academic.oup.com/mnras/pages/general_instructions) ·
  [A&A](https://www.aanda.org/for-authors) ·
  [AAS Journals](https://journals.aas.org/graphics-guide/) ·
  [OJA](https://astro.theoj.org/site/instructions)
