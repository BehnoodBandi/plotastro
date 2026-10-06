# Colours

## The default palette

```{image} _figures/palette.png
:alt: The default colour-blind-friendly cycle
:width: 85%
```

The default cycle has 12 colours, all accessible by name via
`plotastro.COLORS` (e.g. `pa.COLORS["blue"]`), or as matplotlib's
`"C0"`…`"C11"` shorthands:

- **C0–C8** are a colour-blind-safe re-ordering of the
  [ColorBrewer](https://colorbrewer2.org) *Set1* qualitative palette
  (popularised by [Thøger Rivera-Thorsen's CBcycle](https://gist.github.com/thriveth/8560036)).
  Consecutive colours differ in **lightness as well as hue**, so adjacent
  lines stay distinguishable under the common deficiencies (deuteranopia,
  protanopia) *and* in greyscale print; the notorious red–green pair is
  pushed far apart in the cycle (green is C2, red is C7), so plots with a
  handful of lines never rely on it.
- **C9–C11** are light companions (from Tableau's *Color Blind 10*): use
  them for uncertainty bands, reference curves, or de-emphasised data
  underneath a saturated line of the same hue.

## Matched shades without transparency

Better for print and EPS than `alpha=` (no colour shifts where elements
overlap):

```python
ax.plot(x, y, color=pa.COLORS["blue"])
ax.fill_between(x, lo, hi, color=pa.lighten(pa.COLORS["blue"], 0.7))
pa.darken(pa.COLORS["orange"], 0.3)     # the other direction
```

## More palettes

- `pa.OKABE_ITO` — [Okabe & Ito (2008)](https://jfly.uni-koeln.de/color/),
  *the* classic CVD-safe recommendation for categorical colours in science;
- `pa.PETROFF10` — [Petroff (2021)](https://arxiv.org/abs/2107.02270), the
  CVD-optimised 10-colour cycle used across particle physics;
- `pa.PETROFF8` — Petroff's 8-colour sibling, the default cycle of the
  Euclid Consortium's [niceplots](https://gitlab.euclid-sgs.uk/ECEB/niceplots)
  (and of the `euclid` style here);
- `pa.TOL_VIBRANT` — [Paul Tol's](https://personal.sron.nl/~pault/) *vibrant*
  qualitative scheme, 7 CVD-safe colours;
- `pa.PAIRED` — light/dark pairs for data/model or before/after
  comparisons: `pa.PAIRED["blue"]` → `("#a6cee3", "#1f78b4")`.

Any of them can become the active cycle when you activate a style —
`pa.set_style("mnras", palette="okabe_ito")` — or pass your own list of
colours.

## Euclid colour schemes

The `euclid` style (see {doc}`journals`) and these colour schemes are
adapted from the Euclid Consortium Editorial Board's
[niceplots](https://gitlab.euclid-sgs.uk/ECEB/niceplots) (Euclid-internal,
GPL-3.0): the colours are re-expressed here, nothing is copied from it.
{func}`plotastro.euclid_colors` returns each scheme under its niceplots name:

| scheme | colours |
|---|---|
| `"categorical1"` | Petroff (2021) 8 colours — `pa.PETROFF8`; the Euclid default |
| `"categorical2"` | Okabe & Ito — `pa.OKABE_ITO` |
| `"categorical3"` | black, then Tol's *vibrant* scheme — `pa.TOL_VIBRANT` |
| `"sequential"` | `n` colours of increasing brightness from `copper` |
| `"diverging"` | `n` colours from blue to red from `coolwarm` |

```python
pa.set_style("euclid", palette="categorical3")                 # by name
ax.set_prop_cycle(color=pa.euclid_colors("sequential", n=6))   # per axes
```

## Checking accessibility yourself

```{image} _figures/cvd_check.png
:alt: The default palette under simulated colour-vision deficiencies
:width: 85%
```

Don't take the palette's word for it — simulate it (Machado et al. 2009
model, no extra dependencies):

```python
pa.check_colors()                 # any palette under deuteranopia/protanopia/greyscale
pa.check_colors(pa.PAIRED)        # works on your own colour lists/dicts too
pa.check_figure(fig)              # simulate a whole rendered figure — the
                                  # final check before submission
pa.simulate_cvd("#e41a1c", "deuteranopia")   # the raw transform
```

If two lines merge in any panel, add markers or dash patterns (see
{doc}`markers`), or pick colours further apart in the cycle. MNRAS
recommends [Color Oracle](https://colororacle.org) and ColorBrewer for
exactly this; with plotastro it's built in.

## Colormaps

The styles default to `viridis` (perceptually uniform, CVD-safe). Good
picks: `viridis`/`magma`/`cividis` for sequential data, `RdBu_r` or
`coolwarm` for diverging data (red–*blue*, not red–green). Avoid
`jet`/`rainbow`. For more astro-friendly maps see
[cmasher](https://cmasher.readthedocs.io) and
[cmocean](https://matplotlib.org/cmocean/).
