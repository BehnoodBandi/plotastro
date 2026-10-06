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
`jet`/`rainbow`. To change the default for every `imshow`, `pcolormesh`,
`scatter`, … pass `cmap=` when you activate a style:

```python
pa.set_style("mnras", cmap="cividis")
```

For many more maps, plotastro can use CMasher (next section); see also
[cmocean](https://matplotlib.org/cmocean/).

## CMasher colours and colormaps (optional)

```{image} _figures/cmasher.png
:alt: A CMasher colour cycle for a family of lines, and a CMasher colormap on an image
:width: 100%
```

[CMasher](https://cmasher.readthedocs.io) (van der Velden 2020,
[JOSS 5, 2004](https://doi.org/10.21105/joss.02004)) is a collection of
scientific colormaps: sequential, diverging and cyclic, all designed to be
perceptually uniform, and most of them colour-vision-deficiency friendly.
plotastro can use them for discrete colours and for colormaps. CMasher is
**not** a dependency of plotastro: install it only if you want it,

```bash
pip install cmasher                # or: pip install "plotastro[cmasher]"
```

and plotastro imports it only when you ask for a CMasher colour. Every
other feature works the same without it. CMasher names start with
`cmr.` (`"cmr.rainforest"`, `"cmr.iceburn"`, …), which is also how its
maps are registered with matplotlib; append `_r` for the reversed map.
Browse them all in the
[CMasher colormap overview](https://cmasher.readthedocs.io), or list them
with `cmasher.get_cmap_list()`.

### Discrete colours

Pass a `"cmr."` name as the palette to get a colour cycle of 8 colours
sampled from that map, or use {func}`plotastro.cmasher_colors` for a
different number:

```python
pa.set_style("mnras", palette="cmr.rainforest")              # 8-colour cycle
ax.set_prop_cycle(color=pa.cmasher_colors("torch", n=5))     # 5, this axes only
colors = pa.cmasher_colors("ocean", n=4, cmap_range=(0.2, 0.8))
```

The colours are hex strings, equally spaced over `cmap_range`. Its default,
`(0.15, 0.85)`, follows CMasher's own advice: most of its sequential maps
run from black to white, and those ends disappear against the axes or the
page. Sequential maps work best for lines. CMasher recommends:

- **for lines that must be easy to tell apart:** maps with a large
  perceptual range, such as `apple`, `chroma`, `neon`, `rainforest` and
  `torch`;
- **for lines that are steps of one quantity** (redshifts, masses, …): a
  single-hue map, such as `flamingo`, `freeze`, `gothic`, `jungle` and
  `ocean`.

These cycles are ordered from dark to light, and a matplotlib cycle starts
at the first colour. So for a fixed number of lines, sample exactly that
many, `pa.cmasher_colors("rainforest", n=len(models))`, and they will span
the whole map. Check the result with `pa.check_colors(...)` as for any other
palette.

### Colormaps

Make a CMasher map the default colormap with `set_style(cmap=...)`, or get
the colormap itself with {func}`plotastro.cmasher_cmap`. It can also cut
the map to part of its range, or split it into a few discrete levels:

```python
pa.set_style("mnras", cmap="cmr.ocean")            # default for imshow etc.

ax.imshow(img, cmap=pa.cmasher_cmap("rainforest"))
ax.pcolormesh(x, y, z, cmap=pa.cmasher_cmap("ocean", cmap_range=(0.15, 0.85)))
ax.contourf(x, y, z, levels=6, cmap=pa.cmasher_cmap("iceburn", n=6))
```

Once CMasher has been imported (by plotastro or by `import cmasher`), every
matplotlib function also accepts its maps by name: `cmap="cmr.iceburn"`.
Some of CMasher's diverging maps (`iceburn`, `redshift`, `seaweed`,
`watermelon`, `wildfire`) have a **black** centre instead of a white one.

If you use CMasher in a paper, please cite it; `cmasher.get_bibtex()`
prints the reference.
