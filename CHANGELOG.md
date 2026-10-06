# Changelog

## Unreleased

### Added
- `latex_table(data, ...)` returns a LaTeX table for a pandas DataFrame,
  an astropy Table/QTable, a NumPy structured or 2D array, or a dict of
  columns. Each column has its own precision (`sig=` significant figures
  or `decimals=`) and `notation=` (`"fixed"`, `"sci"`, or `"auto"`, which
  is chosen per column). `errors=` merges error columns into their value
  column as `value \pm err`, or as `value^{+hi}_{-lo}` for asymmetric
  errors. The error's significant figures set the value's precision.
  Also: headers, a units row (filled in automatically from astropy
  units), `table`/`table*`/bare `tabular`, optional booktabs rules, and
  missing or masked values. pandas and astropy are not dependencies.

## 1.1.0b2 — 2026-10-06 (beta)

A pre-release: `pip install plotastro` still gives the stable 1.0.1. To try
this beta, use `pip install --pre plotastro` (or `pip install
"plotastro==1.1.0b2"`).

### Changed
- Legends now sit on a translucent white background (70 % opaque, no
  border) instead of none, so they stay readable over data and grid
  lines. The `euclid` style keeps niceplots' framed legends.

## 1.1.0b1 — 2026-10-06 (beta)

A pre-release: `pip install plotastro` still gives the stable 1.0.1. To try
this beta, use `pip install --pre plotastro` (or `pip install
"plotastro==1.1.0b1"`).

### Added
- `euclid` style (alias `ec`) for Euclid Consortium papers, adapted from
  the Euclid Consortium Editorial Board's
  [niceplots](https://gitlab.euclid-sgs.uk/ECEB/niceplots) (GPL-3.0,
  Euclid-internal): sans-serif 10 pt text with Computer Modern maths, no
  grid or minor ticks, framed legends, Petroff-8 colours, and niceplots'
  4 × 3 in figure convention (LaTeX scales the figure into the A&A
  column). The settings are re-expressed in plotastro's own template;
  nothing is copied from niceplots.
- Palettes `PETROFF8` and `TOL_VIBRANT`, and `euclid_colors(scheme, n=)`
  giving niceplots' five colour schemes under their niceplots names.
- `set_style(..., palette=...)` swaps the colour cycle for any named
  palette or list of colours.
- Optional [CMasher](https://cmasher.readthedocs.io) support, for discrete
  colours and colormaps: `cmasher_colors(cmap, n=8, cmap_range=(0.15, 0.85))`
  samples colours from a CMasher map, `cmasher_cmap(cmap, cmap_range=, n=)`
  returns the map (optionally cut, or split into `n` levels), and
  `set_style` accepts `palette="cmr.<name>"`. CMasher is **not** a
  dependency: install it with `pip install "plotastro[cmasher]"` (or
  `pip install cmasher`). plotastro imports it only when one of these is
  used, and without it they raise an `ImportError` saying how to install it.
- `set_style(..., cmap=...)` sets the default colormap: any matplotlib
  name, or `"cmr.<name>"` for CMasher.

### Changed
- `figsize()` / `subplots()`: the default `aspect` now comes from the
  journal (golden ratio everywhere except `euclid`, which uses 4:3).
- `authorlist(..., journal="euclid")` uses the A&A format (Euclid's
  `aaEC` class).

### Fixed
- Switching styles in one session no longer carries settings over.
  matplotlib only overwrites the rcParams a style names, and the styles
  named different ones: after `euclid`, for example, `set_style("mnras")`
  or `plt.style.use("mnras")` kept Euclid's tick padding. Every style now
  sets the same rcParams, using matplotlib's defaults where they apply,
  and a test checks this.

## 1.0.1 — 2026-09-01

### Added
- Documentation site (Sphinx + Furo on Read the Docs) with the rendered
  tutorial notebook and a full API reference:
  <https://plotastro.readthedocs.io>.

No changes to the package code itself.

## 1.0.0 — 2026-09-01

First release as an installable package, `plotastro`.

### Added
- `pip install plotastro`; importing it registers all styles with
  matplotlib, so `plt.style.use("mnras")` works everywhere.
- Journal styles: **MNRAS**, **RASTI**, **A&A**, **ApJ/ApJL (AASTeX)**,
  **Open Journal of Astrophysics**, **PRD/PRL (REVTeX)**, **JCAP**, and
  **Nature Astronomy** (sans-serif variant), plus `thesis`/`beamer`
  width presets. All generated from one template
  (`tools/generate_styles.py`) so they stay consistent.
- Helpers: `set_style`, `figsize`, `subplots`, `savefig`,
  `style_cycler`, `lighten`/`darken`, `label_panels` (journal-style
  (a)/(b)/(c) panel labels), reference charts
  (`show_colors`/`show_markers`/`show_linestyles`).
- Colour-vision-deficiency checking: `simulate_cvd`, `check_colors`,
  and `check_figure` (Machado et al. 2009 model; no extra dependencies).
- Palettes: the default colour-blind-friendly cycle (`COLORS`), Okabe &
  Ito (`OKABE_ITO`), Petroff-10 (`PETROFF10`) and light/dark pairs
  (`PAIRED`).
- Author-list generator: `authorlist("authors.csv", journal=...)` and the
  `plotastro-authors` command-line tool turn a CSV of names/affiliations/
  ORCIDs/emails into the journal's LaTeX author block (MNRAS, A&A,
  AASTeX, REVTeX, JCAP and generic formats), with automatic affiliation
  numbering and sharing. Reads real collaboration lists as-is
  (`Authorname`/`Firstname`+`Lastname` columns, one row per affiliation,
  embedded LaTeX accents, extra columns ignored).
- Zero-learning-curve mode: importing plotastro registers every style
  with matplotlib, so `plt.style.use("mnras")` + ordinary matplotlib is
  the entire integration (`pa.use(...)` is an alias of `set_style`).
- `requirements.txt` / `requirements-dev.txt` for pip users; NumPy 1.x
  and 2.x both supported and tested in CI.
- Tests (pytest), CI and PyPI-publishing GitHub Actions workflows,
  executed tutorial notebook, MIT license.

### Changed
- Styles no longer require LaTeX: portable STIX mathtext by default,
  with `set_style(..., usetex=True)` to opt in (newtx fonts).
- Submission-safe saving defaults: PDF, tight bbox, 450 dpi,
  TrueType font embedding (`pdf.fonttype 42`).

### Migration from the original repo
- `MNRAS_Style.mplstyle` → `plt.style.use("mnras")` (after `import plotastro`).
- `myfigsize.set_size(...)` → `plotastro.set_size(...)` still works, but
  prefer `plotastro.figsize(...)` / `plotastro.subplots(...)`.
