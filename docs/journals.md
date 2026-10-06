# Supported journals

{func}`plotastro.set_style`, {func}`plotastro.figsize` and
`plt.style.use(...)` accept these keys (aliases in parentheses):

| key | journal | one column | full width |
|---|---|---|---|
| `mnras` | Monthly Notices of the RAS | 240.0 pt = 3.32 in | 504.0 pt = 6.97 in |
| `rasti` | RAS Techniques & Instruments | 240.0 pt = 3.32 in | 504.0 pt = 6.97 in |
| `aanda` (`a&a`, `aa`) | Astronomy & Astrophysics | 250.4 pt = 3.46 in (88 mm) | 512.2 pt = 7.09 in (180 mm) |
| `apj` (`apjl`, `aastex`) | The Astrophysical Journal | 242.3 pt = 3.35 in | 513.1 pt = 7.10 in |
| `oja` | Open Journal of Astrophysics | ≈245.3 pt = 3.39 in | ≈508 pt = 7.03 in |
| `prd` (`prl`, `revtex`) | Physical Review D | 246.0 pt = 3.40 in | 510.0 pt = 7.06 in |
| `jcap` | J. Cosmology & Astroparticle Phys. | single-column ≈455 pt = 6.30 in | — |
| `natastro` (`nature`) | Nature Astronomy (sans-serif!) | 253.2 pt = 3.50 in (89 mm) | 520.7 pt = 7.20 in (183 mm) |
| `euclid` (`ec`) | Euclid Consortium papers (A&A; niceplots look, sans-serif) - not recomended!| drawn 4.00 in = 289.1 pt, LaTeX scales it to 88 mm | 8.00 in = 578.2 pt (2 × column) |
| `thesis` | A4 thesis text width | 426.8 pt = 5.91 in | — |
| `beamer` | Beamer slide text width | 307.3 pt = 4.25 in | — |

Widths come from each journal's LaTeX class or author guide. All styles
share the same fonts, colours, tick and legend settings; only the figure
width differs — except Nature Astronomy, which switches to the sans-serif
fonts and smaller (5–7 pt) lettering Nature's figure guide requires, and
the Euclid style, described next.

## Euclid Consortium papers

`pa.set_style("euclid")` ({func}`plotastro.set_style`) reproduces the look of
[niceplots](https://gitlab.euclid-sgs.uk/ECEB/niceplots), the Euclid
Consortium Editorial Board's matplotlib style for Euclid papers
(Euclid-internal, GPL-3.0; set up by Lukas Hergt, with tweaks by Laila
Linke). The style and its colour schemes are **adapted from that
repository**: the settings are re-expressed in plotastro's own template and
nothing is copied from it. How it differs from the other styles:

- sans-serif text at 10 pt with Computer Modern maths, no grid, no minor
  ticks, framed legends, and `axes.xmargin = 0`;
- the default cycle is Petroff's 8-colour palette (`pa.PETROFF8`);
  niceplots' other schemes are available under their niceplots names —
  `pa.set_style("euclid", palette="categorical3")` or
  `pa.euclid_colors("sequential", n=6)` (see {doc}`colors`);
- **sizing follows niceplots rather than the exact-size approach**: figures
  are drawn 4 × 3 in (two-column: 8 × 6 in) and LaTeX scales them into the
  88 mm A&A column, so the 10 pt lettering prints at ≈ 8.7 pt. Include them
  with `\includegraphics[width=\columnwidth]{fig.pdf}`. For a figure at
  its exact printed size with the Euclid look, size it for A&A instead:
  `pa.subplots(journal="aanda")`.

`pa.set_style("euclid", usetex=True)` gives niceplots' LaTeX rendering
(Computer Modern Sans text). Euclid papers use A&A's `aaEC` class, so
`pa.authorlist(..., journal="euclid")` produces the A&A author block.

## Custom documents

For your own document (custom class, thesis template, ...), put
`\the\columnwidth` or `\the\textwidth` anywhere in the `.tex` body, compile,
read the value off the page, and pass it directly:

```python
pa.figsize(width=345.0)          # width in LaTeX points (1 pt = 1/72.27 in)
```

## Per-journal submission notes

| journal | accepted figure formats | notes |
|---|---|---|
| MNRAS / RASTI | EPS preferred, PDF/TIFF fine | ≥ 400 dpi raster, ~8 pt lettering, colour-blind friendly required |
| A&A | PDF/EPS | figures 88 mm (column) or 170–180 mm (page) wide |
| ApJ / AAS | PDF/EPS/PNG | vector strongly preferred |
| OJA | PDF (arXiv-ready) | whatever compiles on arXiv works |
| PRD / JCAP | PDF/EPS | vector preferred |
| Nature Astronomy | PDF/EPS/AI | sans-serif fonts, 5–7 pt lettering |
| Euclid (A&A) | PDF | niceplots look: 4 × 3 in at 10 pt, scaled by LaTeX into the 88 mm column |

Official guidelines:
[MNRAS](https://academic.oup.com/mnras/pages/general_instructions) ·
[A&A](https://www.aanda.org/for-authors) ·
[AAS Journals](https://journals.aas.org/graphics-guide/) ·
[OJA](https://astro.theoj.org/site/instructions) ·
[APS](https://journals.aps.org/authors) ·
[Nature](https://www.nature.com/nature/for-authors/formatting-guide) ·
[Euclid niceplots](https://gitlab.euclid-sgs.uk/ECEB/niceplots) (Euclid-internal)
