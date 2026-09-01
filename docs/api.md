# API reference

Everything is available at the top level:

```python
import plotastro as pa
```

## Styles and sizing

```{eval-rst}
.. autofunction:: plotastro.set_style
.. autofunction:: plotastro.figsize
.. autofunction:: plotastro.subplots
.. autofunction:: plotastro.savefig
.. autofunction:: plotastro.current_journal
```

`pa.use(...)` is an alias of {func}`plotastro.set_style`.

## Colours

```{eval-rst}
.. autofunction:: plotastro.lighten
.. autofunction:: plotastro.darken
.. autofunction:: plotastro.simulate_cvd
.. autofunction:: plotastro.check_colors
.. autofunction:: plotastro.check_figure
```

### Palette constants

| name | contents |
|---|---|
| `pa.COLORS` | the default 12-colour colour-blind-friendly cycle, by name |
| `pa.CYCLE` | the same colours as an ordered list |
| `pa.OKABE_ITO` | Okabe & Ito (2008) 8-colour CVD-safe palette |
| `pa.PETROFF10` | Petroff (2021) 10-colour CVD-optimised palette |
| `pa.PAIRED` | light/dark pairs: `pa.PAIRED["blue"] -> (light, dark)` |

## Markers, line styles and labels

```{eval-rst}
.. autofunction:: plotastro.style_cycler
.. autofunction:: plotastro.label_panels
```

| name | contents |
|---|---|
| `pa.MARKERS` | marker sequence that stays distinguishable at 4 pt |
| `pa.LINESTYLES` | named dash patterns beyond matplotlib's built-ins |

## Reference charts

```{eval-rst}
.. autofunction:: plotastro.show_colors
.. autofunction:: plotastro.show_markers
.. autofunction:: plotastro.show_linestyles
```

## Author lists

```{eval-rst}
.. autofunction:: plotastro.authorlist
```

The `plotastro-authors` command-line tool wraps this function; run
`plotastro-authors --help` for its options.

## Journal data and legacy

```{eval-rst}
.. autofunction:: plotastro.set_size
```

| name | contents |
|---|---|
| `pa.JOURNALS` | per-journal column/full widths (LaTeX points) and metadata |
| `pa.GOLDEN` | the golden ratio (default figure aspect), ≈ 0.618 |
| `pa.STYLE_DIR` | path to the bundled `.mplstyle` files |
