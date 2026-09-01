"""paperplot — publication-quality matplotlib figures for astronomy journals.

One import gives you journal-matched styles, correctly sized figures and a
colour-blind-friendly palette:

    import matplotlib.pyplot as plt
    import paperplot as pp

    pp.set_style("mnras")                     # or "aanda", "apj", "oja"
    fig, ax = pp.subplots()                   # one-column, golden-ratio figure
    ax.plot(x, y, label="model")
    ax.set_xlabel("$x$")
    ax.legend()
    pp.savefig("myplot")                      # -> myplot.pdf

Supported journals: MNRAS, A&A, ApJ/ApJL (AASTeX), the Open Journal of
Astrophysics — plus "thesis" and "beamer" width presets. See README.md for
the full tutorial.
"""

from __future__ import annotations

import colorsys
import functools
import operator
from pathlib import Path

import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from cycler import cycler

__all__ = [
    "set_style", "figsize", "subplots", "savefig",
    "COLORS", "CYCLE", "OKABE_ITO", "MARKERS", "LINESTYLES",
    "style_cycler", "lighten", "darken",
    "show_colors", "show_markers", "show_linestyles",
    "JOURNALS", "GOLDEN", "set_size",
]

STYLE_DIR = Path(__file__).resolve().parent / "styles"

#: Golden ratio (height/width) used for default figure heights.
GOLDEN = (5 ** 0.5 - 1) / 2  # 0.618...

#: Text-block widths in LaTeX points (1 pt = 1/72.27 inch) per journal,
#: and the style sheet each journal uses.
JOURNALS = {
    "mnras":  {"column": 240.0,     "full": 504.0,     "style": "mnras",
               "name": "Monthly Notices of the RAS"},
    "aanda":  {"column": 250.38,    "full": 512.15,    "style": "aanda",
               "name": "Astronomy & Astrophysics"},
    "apj":    {"column": 242.26653, "full": 513.11743, "style": "apj",
               "name": "The Astrophysical Journal (AASTeX)"},
    "oja":    {"column": 245.26653, "full": 508.0,     "style": "oja",
               "name": "The Open Journal of Astrophysics"},
    # Not journals, but handy width presets (they use the MNRAS look):
    "thesis": {"column": 426.79135, "full": 426.79135, "style": "mnras",
               "name": "A4 thesis text width"},
    "beamer": {"column": 307.28987, "full": 307.28987, "style": "mnras",
               "name": "Beamer slide text width"},
}

_ALIASES = {
    "a&a": "aanda", "aa": "aanda", "astronomy&astrophysics": "aanda",
    "apjl": "apj", "aas": "apj", "aastex": "apj", "aj": "apj",
    "openjournal": "oja", "theoj": "oja", "openjournalofastrophysics": "oja",
    "mnras_full": "mnras",  # legacy name from myfigsize.set_size
}

_state = {"journal": "mnras"}


def _resolve(journal):
    key = str(journal).lower().replace(" ", "").replace("-", "")
    key = _ALIASES.get(key, key)
    if key not in JOURNALS:
        options = ", ".join(sorted(JOURNALS))
        raise ValueError(f"Unknown journal {journal!r}. Choose one of: {options}")
    return key


# ----------------------------------------------------------------------
# Style activation
# ----------------------------------------------------------------------

def set_style(journal="mnras", *, usetex=False, grid=None, **rc_overrides):
    """Activate the plotting style for a journal.

    Parameters
    ----------
    journal : str
        One of ``"mnras"``, ``"aanda"`` (aliases ``"a&a"``, ``"aa"``),
        ``"apj"`` (aliases ``"apjl"``, ``"aastex"``), ``"oja"``,
        ``"thesis"`` or ``"beamer"``.
    usetex : bool, optional
        If True, render all text with a real LaTeX installation using
        Times-compatible newtx fonts. Default False (portable mathtext).
    grid : bool, optional
        Override the style's grid setting (the styles default to a
        subtle grid; pass ``grid=False`` for a clean journal look).
    **rc_overrides
        Any extra rcParams, e.g. ``set_style("mnras", **{"font.size": 10})``.

    Examples
    --------
    >>> pp.set_style("aanda")
    >>> pp.set_style("mnras", usetex=True, grid=False)
    """
    key = _resolve(journal)
    style_file = STYLE_DIR / f"{JOURNALS[key]['style']}.mplstyle"
    plt.style.use(style_file)
    _state["journal"] = key
    if usetex:
        mpl.rcParams.update({
            "text.usetex": True,
            "text.latex.preamble": r"\usepackage{newtxtext}\usepackage{newtxmath}",
        })
    if grid is not None:
        mpl.rcParams["axes.grid"] = bool(grid)
    if rc_overrides:
        mpl.rcParams.update(rc_overrides)


# ----------------------------------------------------------------------
# Figure sizing
# ----------------------------------------------------------------------

def figsize(width="column", *, journal=None, fraction=1.0, nrows=1, ncols=1,
            aspect=GOLDEN, height=None):
    """Figure dimensions (inches) that match the journal's text layout,
    so the figure is never rescaled (and its fonts shrunk) by LaTeX.

    Parameters
    ----------
    width : {"column", "full"} or float
        ``"column"`` for a one-column figure, ``"full"`` for the full
        text width, or a number = a custom width in LaTeX points
        (get yours with ``\\the\\columnwidth`` in your .tex file).
    journal : str, optional
        Journal to size for; defaults to the one from the last
        :func:`set_style` call.
    fraction : float, optional
        Fraction of that width to occupy (e.g. 0.5 for half a column).
    nrows, ncols : int, optional
        Subplot grid shape; the height scales so each panel keeps the
        requested aspect ratio.
    aspect : float, optional
        Height/width ratio of one panel. Default: golden ratio (0.618).
        Use ``aspect=1`` for square panels.
    height : float, optional
        Explicit figure height in inches (overrides ``aspect``).

    Returns
    -------
    (width_in, height_in) : tuple of float
    """
    key = _resolve(journal) if journal is not None else _state["journal"]
    if isinstance(width, str):
        w = width.lower()
        if w in ("column", "col", "onecolumn", "one", "single"):
            width_pt = JOURNALS[key]["column"]
        elif w in ("full", "fullwidth", "two", "twocolumn", "page", "text"):
            width_pt = JOURNALS[key]["full"]
        else:
            raise ValueError(
                f"width must be 'column', 'full' or a number of points, got {width!r}")
    else:
        width_pt = float(width)

    fig_width_in = width_pt * fraction / 72.27
    if height is not None:
        fig_height_in = float(height)
    else:
        fig_height_in = fig_width_in * aspect * (nrows / ncols)
    return (fig_width_in, fig_height_in)


def subplots(nrows=1, ncols=1, *, width="column", journal=None, fraction=1.0,
             aspect=GOLDEN, height=None, **kwargs):
    """`plt.subplots` with the figure size computed by :func:`figsize`.

    Examples
    --------
    >>> fig, ax = pp.subplots()                          # one-column figure
    >>> fig, axes = pp.subplots(2, 2, width="full")      # full-width 2x2 grid
    >>> fig, ax = pp.subplots(aspect=1)                  # square panel
    """
    if "figsize" not in kwargs:
        kwargs["figsize"] = figsize(width, journal=journal, fraction=fraction,
                                    nrows=nrows, ncols=ncols, aspect=aspect,
                                    height=height)
    return plt.subplots(nrows, ncols, **kwargs)


def savefig(name, fig=None, formats=("pdf",), **kwargs):
    """Save a figure under one or more formats at once.

    Parameters
    ----------
    name : str or Path
        Output path without extension (a known extension is stripped).
    fig : Figure, optional
        Defaults to the current figure.
    formats : sequence of str, optional
        e.g. ``("pdf", "png")`` to get both a vector file for the paper
        and a raster preview.
    **kwargs
        Forwarded to ``fig.savefig`` (e.g. ``dpi=600``).

    Returns
    -------
    list of str : the files written.
    """
    fig = fig if fig is not None else plt.gcf()
    base = Path(name)
    if base.suffix.lower() in (".pdf", ".png", ".eps", ".svg", ".jpg", ".tiff"):
        formats = (base.suffix[1:],)
        base = base.with_suffix("")
    written = []
    for ext in formats:
        out = f"{base}.{ext}"
        fig.savefig(out, **kwargs)
        written.append(out)
    return written


# ----------------------------------------------------------------------
# Colours
# ----------------------------------------------------------------------

#: The default colour-blind-friendly cycle, by name (see README.md).
#: First 9: reordered ColorBrewer "Set1" made colour-blind safe;
#: last 3: light companions from Tableau's Color Blind 10 palette.
COLORS = {
    "blue":        "#377eb8",
    "orange":      "#ff7f00",
    "green":       "#4daf4a",
    "pink":        "#f781bf",
    "brown":       "#a65628",
    "purple":      "#984ea3",
    "grey":        "#999999",
    "red":         "#e41a1c",
    "yellow":      "#dede00",
    "lightblue":   "#a2c8ec",
    "lightorange": "#ffbc79",
    "lightgrey":   "#ababab",
}

#: The colours of the default cycle, in order.
CYCLE = list(COLORS.values())

#: Okabe & Ito (2008) palette — an alternative 8-colour scheme designed
#: for all common types of colour-vision deficiency.
OKABE_ITO = {
    "black":      "#000000",
    "orange":     "#e69f00",
    "skyblue":    "#56b4e9",
    "green":      "#009e73",
    "yellow":     "#f0e442",
    "blue":       "#0072b2",
    "vermillion": "#d55e00",
    "purple":     "#cc79a7",
}


def lighten(color, amount=0.5):
    """Lighten a colour by moving it towards white (0 = unchanged, 1 = white).

    Handy for e.g. filled uncertainty bands under a line of the same hue:

    >>> ax.plot(x, y, color=pp.COLORS["blue"])
    >>> ax.fill_between(x, lo, hi, color=pp.lighten(pp.COLORS["blue"], 0.7))
    """
    h, l, s = colorsys.rgb_to_hls(*mcolors.to_rgb(color))
    return colorsys.hls_to_rgb(h, l + (1 - l) * amount, s)


def darken(color, amount=0.5):
    """Darken a colour by moving it towards black (0 = unchanged, 1 = black)."""
    h, l, s = colorsys.rgb_to_hls(*mcolors.to_rgb(color))
    return colorsys.hls_to_rgb(h, l * (1 - amount), s)


# ----------------------------------------------------------------------
# Markers and line styles
# ----------------------------------------------------------------------

#: A marker sequence that stays distinguishable at small sizes.
MARKERS = ["o", "s", "^", "D", "v", "p", "*", "X"]

#: Named dash patterns. The tuples are matplotlib (offset, (on, off, ...))
#: dash specs — they scale with the line width and print cleanly.
LINESTYLES = {
    "solid":            "-",
    "dashed":           (0, (5, 2)),
    "dotted":           (0, (1, 1.5)),
    "dashdot":          (0, (5, 2, 1, 2)),
    "long dash":        (0, (9, 3)),
    "dash dot dot":     (0, (5, 2, 1, 2, 1, 2)),
    "densely dotted":   (0, (1, 0.8)),
    "loosely dashed":   (0, (5, 6)),
}


def style_cycler(n=None, *, colors=True, markers=False, linestyles=False):
    """Build a property cycler that pairs colours with markers and/or
    dash patterns, so lines stay distinguishable in greyscale and for
    colour-blind readers (redundant encoding).

    Parameters
    ----------
    n : int, optional
        Number of entries (default: length of the colour cycle, or 8
        when markers/linestyles are included).
    colors, markers, linestyles : bool
        Which properties to cycle together.

    Examples
    --------
    >>> ax.set_prop_cycle(pp.style_cycler(markers=True))
    >>> ax.set_prop_cycle(pp.style_cycler(linestyles=True))
    >>> plt.rc("axes", prop_cycle=pp.style_cycler(markers=True))  # globally
    """
    if n is None:
        n = len(CYCLE) if not (markers or linestyles) else min(len(CYCLE), 8)
    parts = []
    if colors:
        parts.append(cycler(color=(CYCLE * 3)[:n]))
    if markers:
        parts.append(cycler(marker=(MARKERS * 3)[:n]))
    if linestyles:
        parts.append(cycler(linestyle=(list(LINESTYLES.values()) * 3)[:n]))
    if not parts:
        raise ValueError("Enable at least one of colors/markers/linestyles.")
    return functools.reduce(operator.add, parts)


# ----------------------------------------------------------------------
# Reference charts (used in the tutorial and README)
# ----------------------------------------------------------------------

def show_colors(palette=None, title="Default colour-blind-friendly cycle"):
    """Swatch chart of a palette dict (default: the style's colour cycle)."""
    palette = palette if palette is not None else COLORS
    names = list(palette)
    fig, ax = plt.subplots(figsize=figsize("full", fraction=0.9, height=0.32 * len(names) + 0.5))
    ax.set_axis_off()
    ax.set_title(title)
    for i, name in enumerate(names):
        y = len(names) - 1 - i
        ax.add_patch(plt.Rectangle((0, y + 0.1), 1.6, 0.8,
                                   color=palette[name], ec="0.2", lw=0.4))
        ax.text(1.75, y + 0.5, f"C{i}  ·  {name}  ·  {str(palette[name]).upper()}",
                va="center", ha="left", fontsize=8, family="monospace")
    ax.set_xlim(0, 6)
    ax.set_ylim(0, len(names))
    return fig


def show_markers():
    """Reference chart of the marker sequence (and a few more)."""
    extra = ["<", ">", "h", "8", "P", "d", "x", "+"]
    all_markers = MARKERS + extra
    fig, ax = plt.subplots(figsize=figsize("full", fraction=0.9, height=1.6))
    ax.set_axis_off()
    ax.set_title("Markers — first row is paperplot.MARKERS")
    for i, m in enumerate(all_markers):
        row, col = divmod(i, 8)
        y = 1.4 - row
        ax.plot(col, y, marker=m, ms=7, color=CYCLE[col % len(CYCLE)],
                ls="none", clip_on=False)
        ax.text(col, y - 0.42, repr(m), ha="center", va="top", fontsize=8,
                family="monospace")
    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(-0.7, 2.0)
    return fig


def show_linestyles():
    """Reference chart of the named dash patterns in LINESTYLES."""
    fig, ax = plt.subplots(figsize=figsize("full", fraction=0.9,
                                           height=0.34 * len(LINESTYLES) + 0.5))
    ax.set_axis_off()
    ax.set_title("Named line styles — paperplot.LINESTYLES")
    for i, (name, ls) in enumerate(LINESTYLES.items()):
        y = len(LINESTYLES) - 1 - i
        ax.plot([0.35, 1.0], [y, y], ls=ls, lw=1.4,
                color=CYCLE[i % len(CYCLE)])
        ax.text(0.32, y, name, ha="right", va="center", fontsize=8)
    ax.set_xlim(0, 1.02)
    ax.set_ylim(-0.6, len(LINESTYLES) - 0.4)
    return fig


# ----------------------------------------------------------------------
# Backwards compatibility with the original myfigsize.set_size()
# ----------------------------------------------------------------------

def set_size(width="mnras", fraction=1, subplots=(1, 1), hight_ratio=1):
    """Deprecated — use :func:`figsize` instead. Kept so old scripts run.

    ``set_size('mnras')`` == ``figsize('column', journal='mnras')`` and
    ``set_size('mnras_full')`` == ``figsize('full', journal='mnras')``.
    """
    if width == "mnras_full":
        return figsize("full", journal="mnras", fraction=fraction,
                       nrows=subplots[0], ncols=subplots[1],
                       aspect=GOLDEN * hight_ratio)
    if isinstance(width, str):
        return figsize("column", journal=width, fraction=fraction,
                       nrows=subplots[0], ncols=subplots[1],
                       aspect=GOLDEN * hight_ratio)
    return figsize(width, fraction=fraction,
                   nrows=subplots[0], ncols=subplots[1],
                   aspect=GOLDEN * hight_ratio)
