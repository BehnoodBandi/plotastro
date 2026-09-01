# Changelog

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
- Documentation site (Sphinx + Furo on Read the Docs) with the rendered
  tutorial notebook and a full API reference:
  <https://plotastro.readthedocs.io>.

### Changed
- Styles no longer require LaTeX: portable STIX mathtext by default,
  with `set_style(..., usetex=True)` to opt in (newtx fonts).
- Submission-safe saving defaults: PDF, tight bbox, 450 dpi,
  TrueType font embedding (`pdf.fonttype 42`).

### Migration from the original repo
- `MNRAS_Style.mplstyle` → `plt.style.use("mnras")` (after `import plotastro`).
- `myfigsize.set_size(...)` → `plotastro.set_size(...)` still works, but
  prefer `plotastro.figsize(...)` / `plotastro.subplots(...)`.
