# Tweaks and FAQ

**How do I turn the grid off?**
`pa.set_style("mnras", grid=False)`, or per-axes `ax.grid(False)`.

**How do I override any other setting?**
`pa.set_style("mnras", **{"font.size": 10})`, or set
`plt.rcParams[...]` after `set_style` — the styles are ordinary
matplotlib rcParams underneath.

**I get a "Times New Roman not found" warning.**
The font list falls back through Times → Nimbus Roman → STIX → DejaVu
automatically; install `mscorefonts`/STIX to silence it, or ignore it.

**My labels are getting cut off.**
They shouldn't be — the styles enable `constrained_layout`. If you manage
layout manually (e.g. `fig.subplots_adjust`), disable it first with
`plt.rcParams["figure.constrained_layout.use"] = False`.

**What about astronomical images?**
Use `origin="lower"` in `imshow` (or uncomment `image.origin: lower` in
the style file), and `ax.grid(False)`.

**Figures look huge/small on my screen.**
That's just `figure.dpi: 150` for display; the size that lands on disk
is exact.

**Can I use the styles without any plotastro code?**
Yes — after `import plotastro` once, `plt.style.use("mnras")` works in any
code; or copy the `.mplstyle` files from `src/plotastro/styles/` into
`matplotlib.get_configdir()/stylelib/` and skip the package entirely.

**I used the original mplstyle_for_MNRAS repo — what changed?**
`plotastro.set_size(...)` reproduces the original `myfigsize.set_size()`
(including the `mnras`/`mnras_full` width names), and the old
`MNRAS_Style.mplstyle` is now `plt.style.use("mnras")`.

**A journal wants EPS and my transparency disappeared.**
EPS has no transparency support. Replace `alpha=` with
`pa.lighten(colour, amount)` shades — opaque, prints identically, and
looks the same on screen.

**Which colormap should I use?**
`viridis` (the default), `magma` or `cividis` for sequential data;
`RdBu_r`/`coolwarm` for diverging data. Avoid `jet` and `rainbow` — they
are not perceptually uniform and are hostile to colour-blind readers.
