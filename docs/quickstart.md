# Quickstart

## Two ways to use plotastro

**Plain matplotlib** — importing plotastro registers the styles with
matplotlib, so this is the entire integration:

```python
import matplotlib.pyplot as plt
import plotastro

plt.style.use("mnras")
fig, ax = plt.subplots()         # already MNRAS column-sized
```

**With the helpers** — journal-aware sizing and saving:

```python
import plotastro as pa

pa.set_style("mnras")            # pa.use(...) is an alias
fig, ax = pa.subplots()
ax.plot(x, y, label="model")
ax.set_xlabel("$x$")
ax.legend()
pa.savefig("myplot")             # -> myplot.pdf
```

Then in LaTeX, include the figure **without any scaling** — that is the
whole point (the fonts come out exactly as designed):

```latex
\begin{figure}
    \includegraphics{myplot.pdf}   % no [width=...] needed!
    \caption{...}
\end{figure}
```

## Figure sizing

{func}`plotastro.figsize` knows the column and full text widths of each
journal (see {doc}`journals`):

```python
pa.figsize("column")                  # one column, golden-ratio height
pa.figsize("full")                    # full text width
pa.figsize("column", fraction=0.5)    # half a column
pa.figsize("column", aspect=1)        # square panel (aspect = height/width)
pa.figsize("column", journal="aanda") # size for a specific journal
pa.figsize(345.0)                     # any width in LaTeX points
```

{func}`plotastro.subplots` takes the same arguments *plus* everything
`plt.subplots` accepts, and scales the height with the grid so each panel
keeps its aspect:

```python
fig, ax   = pa.subplots()                          # 1 panel, one column
fig, axes = pa.subplots(2, 2, width="full")        # 2x2 grid, full width
fig, axes = pa.subplots(1, 2, width="full", aspect=0.75, sharey=True)
```

## Overriding the style

```python
pa.set_style("mnras", grid=False)                  # no grid
pa.set_style("mnras", **{"font.size": 10})         # any rcParam
```

## LaTeX text rendering

By default the styles use matplotlib's built-in *mathtext* with STIX fonts —
Times-compatible maths that works everywhere, with no LaTeX required. For
pixel-perfect agreement with your manuscript:

```python
pa.set_style("mnras", usetex=True)   # needs latex + dvipng + ghostscript
```

This loads the `newtx` Times fonts (matching the MNRAS/A&A house font), or
Helvetica for Nature Astronomy. Develop with `usetex=False`, flip it on for
the final version — LaTeX rendering is slow.

## Saving figures

The styles bake in submission-friendly defaults: **PDF** output, 450 dpi for
rasterised elements, tight bounding box, and TrueType font embedding
(`pdf.fonttype: 42`, so no Type-3 font rejections from submission systems).

```python
pa.savefig("figure1")                              # figure1.pdf
pa.savefig("figure1", formats=("pdf", "png"))      # + a PNG for slides
pa.savefig("figure1", fig=fig, dpi=600)            # extra options pass through
```

If a journal insists on EPS, note EPS has **no transparency** — replace
`alpha=` with {func}`plotastro.lighten` shades (a good habit anyway).

For the full walk-through with plots, see the {doc}`tutorial`.
