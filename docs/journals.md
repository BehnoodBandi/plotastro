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
| `prd` (`prl`, `revtex`) | Physical Review D, and the other *Physical Review* journals (PRL, PRA, PRB, PRC, PRE, PRX, ...), which share its REVTeX layout | 246.0 pt = 3.40 in | 510.0 pt = 7.06 in |
| `jcap` | J. Cosmology & Astroparticle Phys. | single-column ≈455 pt = 6.30 in | — |
| `natastro` (`nature`) | Nature Astronomy (sans-serif!) | 253.2 pt = 3.50 in (89 mm) | 520.7 pt = 7.20 in (183 mm) |
| `rsc` | All Royal Society of Chemistry journals (sans-serif) | 236.2 pt = 3.27 in (8.3 cm) | 486.5 pt = 6.73 in (17.1 cm) |
| `acs` (`jacs`, `achemso`) | All American Chemical Society journals (sans-serif) | 240.9 pt = 3.33 in | 505.9 pt = 7.00 in |
| `thesis` | A4 thesis text width | 426.8 pt = 5.91 in | — |
| `beamer` | Beamer slide text width | 307.3 pt = 4.25 in | — |

Widths come from each journal's LaTeX class or author guide. All styles
share the same fonts, colours, tick and legend settings; only the figure
width differs — except Nature Astronomy, which switches to the sans-serif
fonts and smaller (5–7 pt) lettering Nature's figure guide requires, and
the chemistry styles, described below.

## Chemistry journals (RSC and ACS)

Each chemistry publisher has one figure guide for all its journals, so
there is one style per publisher: `rsc` for every Royal Society of
Chemistry journal (*Chemical Science*, *ChemComm*, *PCCP*, *Dalton
Transactions*, *Journal of Materials Chemistry*, *RSC Advances*, ...) and
`acs` for every American Chemical Society journal (*JACS*, *ACS Nano*,
*The Journal of Physical Chemistry*, *Langmuir*, *Nano Letters*, ...).

- **Widths.** RSC: figures fit a single column (8.3 cm) or a double
  column (17.1 cm), at most 23.3 cm tall. ACS: up to 240 pt (3.33 in) for
  one column, 300–504 pt (4.17–7 in) for two, at most 660 pt (9.17 in)
  tall including the caption. ACS gives these in PostScript points
  (1/72 in), so they are 240.9 and 505.9 LaTeX points here.
- **Fonts.** ACS recommends Helvetica or Arial, so both styles use
  sans-serif fonts (Arial, then Helvetica). Some ACS journals (for
  example *ACS Central Science* and *Environmental Science & Technology*)
  ask for no text smaller than 8 pt, so all text in these styles, tick
  labels and legends included, is 8 pt. RSC sets no font rules, so `rsc`
  uses the same lettering as `acs`.
- **Lines.** ACS asks for no line thinner than 0.5 pt, so the minor ticks
  and grid lines are 0.5 pt here instead of 0.4 pt.
- **Saving.** RSC asks for TIFF at ≥ 600 dpi and accepts PDF or EPS,
  which it converts to TIFF. ACS has graphics placed in the manuscript
  file, at ≥ 300 dpi for colour, 600 dpi for greyscale and 1200 dpi for
  black-and-white line art. The styles save PDF, with 450 dpi for any
  raster parts; for a TIFF, use
  `pa.savefig("fig", formats=("tiff",), dpi=600)`.

{func}`plotastro.authorlist` has no author-list format for these journals
yet; use `journal="generic"` for a plain numbered block.

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
| Physical Review (PRD, PRL, PRB, ...) / JCAP | PDF/EPS | vector preferred |
| Nature Astronomy | PDF/EPS/AI | sans-serif fonts, 5–7 pt lettering |
| RSC journals | TIFF ≥ 600 dpi; PDF/EPS accepted (converted to TIFF) | 8.3 / 17.1 cm wide, ≤ 23.3 cm tall; table-of-contents graphic ≤ 8 × 4 cm |
| ACS journals | placed in the manuscript; ≥ 300 dpi colour, 600 dpi greyscale, 1200 dpi line art | Helvetica/Arial lettering ≥ 4.5 pt (≥ 8 pt in some journals), lines ≥ 0.5 pt; TOC graphic 3.25 × 1.75 in |

Official guidelines:
[MNRAS](https://academic.oup.com/mnras/pages/general_instructions) ·
[A&A](https://www.aanda.org/for-authors) ·
[AAS Journals](https://journals.aas.org/graphics-guide/) ·
[OJA](https://astro.theoj.org/site/instructions) ·
[APS](https://journals.aps.org/authors) ·
[Nature](https://www.nature.com/nature/for-authors/formatting-guide) ·
[RSC](https://www.rsc.org/journals-books-databases/author-and-reviewer-hub/authors-information/prepare-and-format/figures-graphics-images/) ·
[ACS](https://researcher-resources.acs.org/publish/author_guidelines?coden=jacsat) (Appendix 2, "Preparing Graphics"; the same in every ACS journal's guidelines)
