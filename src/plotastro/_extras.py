"""Markers, line styles, property cyclers, panel labels, reference charts."""

from __future__ import annotations

import functools
import operator
import string

import matplotlib.pyplot as plt
from cycler import cycler

from ._colors import COLORS, CYCLE
from ._core import figsize

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
    >>> ax.set_prop_cycle(pa.style_cycler(markers=True))
    >>> ax.set_prop_cycle(pa.style_cycler(linestyles=True))
    >>> plt.rc("axes", prop_cycle=pa.style_cycler(markers=True))  # globally
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
# Panel labels
# ----------------------------------------------------------------------

_PANEL_POSITIONS = {
    # loc: (x, y, ha, va) in axes coordinates
    "upper left":  (0.05, 0.95, "left", "top"),
    "upper right": (0.95, 0.95, "right", "top"),
    "lower left":  (0.05, 0.05, "left", "bottom"),
    "lower right": (0.95, 0.05, "right", "bottom"),
    "outside":     (0.0, 1.02, "left", "bottom"),
}


def label_panels(axes, fmt="({})", loc="upper left", uppercase=False,
                 labels=None, **text_kw):
    """Stamp (a), (b), (c), ... on a grid of subplots, the way most
    journals want multi-panel figures labelled.

    Parameters
    ----------
    axes : Axes, sequence of Axes, or array from plt.subplots
        Labelled in the order given (arrays are flattened row-major).
    fmt : str, optional
        Applied to each letter; e.g. ``"({})"`` -> "(a)", ``"{}."`` -> "a.".
    loc : str, optional
        One of "upper left", "upper right", "lower left", "lower right",
        or "outside" (above the top-left corner — the Nature convention,
        usually combined with ``fmt="{}"`` and bold text).
    uppercase : bool, optional
        Use A, B, C instead of a, b, c.
    labels : sequence of str, optional
        Explicit labels, overriding the alphabet.
    **text_kw
        Forwarded to ``ax.text`` (e.g. ``fontweight="bold"``).

    Returns
    -------
    list of the Text objects created.

    Examples
    --------
    >>> fig, axes = pa.subplots(2, 2, width="full")
    >>> pa.label_panels(axes)
    >>> pa.label_panels(axes, loc="outside", fmt="{}", fontweight="bold")
    """
    if hasattr(axes, "flat"):          # numpy array from plt.subplots
        axes = list(axes.flat)
    elif not hasattr(axes, "__iter__"):
        axes = [axes]
    if loc not in _PANEL_POSITIONS:
        options = ", ".join(_PANEL_POSITIONS)
        raise ValueError(f"loc must be one of: {options}; got {loc!r}")
    x, y, ha, va = _PANEL_POSITIONS[loc]
    letters = string.ascii_uppercase if uppercase else string.ascii_lowercase
    if labels is None:
        labels = [fmt.format(letters[i]) for i in range(len(axes))]
    texts = []
    for ax, label in zip(axes, labels):
        texts.append(ax.text(x, y, label, transform=ax.transAxes,
                             ha=ha, va=va, **text_kw))
    return texts


# ----------------------------------------------------------------------
# Reference charts (used in the tutorial and README)
# ----------------------------------------------------------------------

def show_colors(palette=None, title="Default colour-blind-friendly cycle"):
    """Swatch chart of a palette dict (default: the style's colour cycle)."""
    palette = palette if palette is not None else COLORS
    names = list(palette)
    fig, ax = plt.subplots(
        figsize=figsize("full", journal="mnras", fraction=0.9,
                        height=0.32 * len(names) + 0.5))
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
    fig, ax = plt.subplots(
        figsize=figsize("full", journal="mnras", fraction=0.9, height=1.6))
    ax.set_axis_off()
    ax.set_title("Markers — first row is plotastro.MARKERS")
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
    fig, ax = plt.subplots(
        figsize=figsize("full", journal="mnras", fraction=0.9,
                        height=0.34 * len(LINESTYLES) + 0.5))
    ax.set_axis_off()
    ax.set_title("Named line styles — plotastro.LINESTYLES")
    for i, (name, ls) in enumerate(LINESTYLES.items()):
        y = len(LINESTYLES) - 1 - i
        ax.plot([0.35, 1.0], [y, y], ls=ls, lw=1.4,
                color=CYCLE[i % len(CYCLE)])
        ax.text(0.32, y, name, ha="right", va="center", fontsize=8)
    ax.set_xlim(0, 1.02)
    ax.set_ylim(-0.6, len(LINESTYLES) - 0.4)
    return fig
