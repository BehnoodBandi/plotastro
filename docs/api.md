# API reference

Everything is available at the top level of the package:

```python
import plotastro as pa
```

The reference is split by topic into the pages below, grouped in three
sets. Each table lists everything a page documents. The guides
({doc}`quickstart`, {doc}`colors`, {doc}`markers`, {doc}`authors`) show the
same features in use.

## Figures

**{doc}`api/styles`**

| name | what it does |
|---|---|
| {func}`~plotastro.set_style`, {func}`~plotastro.use` | activate a journal's style, optionally with a palette, colormap, LaTeX or rcParams |
| {func}`~plotastro.current_journal` | the journal of the last `set_style` call |
| {func}`~plotastro.figsize` | figure dimensions matching a journal's column or text width |
| {func}`~plotastro.subplots` | `plt.subplots` with that size computed for you |
| {func}`~plotastro.savefig` | save a figure in several formats at once |
| {data}`~plotastro.JOURNALS`, {data}`~plotastro.GOLDEN`, {data}`~plotastro.STYLE_DIR` | journal widths, the default aspect ratio, the `.mplstyle` files |
| {func}`~plotastro.set_size` | deprecated form of `figsize`, from the original API |

**{doc}`api/markers`**

| name | what it does |
|---|---|
| {data}`~plotastro.MARKERS`, {data}`~plotastro.LINESTYLES` | marker sequence and named dash patterns |
| {func}`~plotastro.style_cycler` | a property cycle pairing colours with markers and/or dashes |
| {func}`~plotastro.label_panels` | (a), (b), (c) panel labels |
| {func}`~plotastro.show_markers`, {func}`~plotastro.show_linestyles` | reference charts of the markers and dash patterns |

## Colours

**{doc}`api/cmasher`** (optional `cmasher` package)

| name | what it does |
|---|---|
| {func}`~plotastro.cmasher_colors` | `n` discrete colours sampled from a CMasher colormap |
| {func}`~plotastro.cmasher_cmap` | a CMasher colormap, optionally cut or split into levels |

**{doc}`api/colors`**

| name | what it does |
|---|---|
| {data}`~plotastro.COLORS`, {data}`~plotastro.CYCLE` | the default colour cycle, by name and in order |
| {data}`~plotastro.OKABE_ITO`, {data}`~plotastro.PETROFF8`, {data}`~plotastro.PETROFF10`, {data}`~plotastro.TOL_VIBRANT`, {data}`~plotastro.PAIRED` | more palettes |
| {func}`~plotastro.lighten`, {func}`~plotastro.darken` | matched shades without transparency |
| {func}`~plotastro.show_colors` | swatch chart of a palette |

**{doc}`api/accessibility`**

| name | what it does |
|---|---|
| {func}`~plotastro.simulate_cvd` | how colours look with a colour-vision deficiency, or in greyscale |
| {func}`~plotastro.check_colors` | a palette next to its simulations |
| {func}`~plotastro.check_figure` | a whole rendered figure next to its simulations |

## LaTeX output

**{doc}`api/authors`**

| name | what it does |
|---|---|
| {func}`~plotastro.authorlist` | LaTeX author/affiliation block for a journal, from a CSV file |
| `plotastro-authors` | the same from the command line |

## Package

`pa.__version__` is the installed version, as a string. Importing
plotastro also registers its styles with matplotlib, so
`plt.style.use("mnras")` works anywhere afterwards (see
{ref}`api-plain-matplotlib`).

```{toctree}
:hidden:
:caption: Figures

api/styles
api/markers
```

```{toctree}
:hidden:
:caption: Colours

api/cmasher
api/colors
api/accessibility
```

```{toctree}
:hidden:
:caption: LaTeX output

api/authors
```
