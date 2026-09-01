"""Palettes, colour utilities and colour-vision-deficiency checking."""

from __future__ import annotations

import colorsys

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from ._core import figsize

# ----------------------------------------------------------------------
# Palettes
# ----------------------------------------------------------------------

#: The default colour-blind-friendly cycle, by name (see the README).
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

#: Okabe & Ito (2008) palette — the classic 8-colour scheme designed
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

#: Petroff (2021) 10-colour palette — the CVD-optimised cycle adopted as
#: matplotlib's "petroff10" style and widely used in particle physics.
PETROFF10 = {
    "blue":   "#3f90da",
    "yellow": "#ffa90e",
    "red":    "#bd1f01",
    "grey":   "#94a4a2",
    "purple": "#832db6",
    "brown":  "#a96b59",
    "orange": "#e76300",
    "tan":    "#b9ac70",
    "slate":  "#717581",
    "cyan":   "#92dadd",
}

#: Light/dark pairs (ColorBrewer "Paired") — ideal for data/model or
#: before/after pairs: PAIRED["blue"] -> (light, dark). Note this palette
#: is *not* fully CVD-safe on its own (it contains red and green); pair
#: it with distinct line styles or markers.
PAIRED = {
    "blue":   ("#a6cee3", "#1f78b4"),
    "green":  ("#b2df8a", "#33a02c"),
    "red":    ("#fb9a99", "#e31a1c"),
    "orange": ("#fdbf6f", "#ff7f00"),
    "purple": ("#cab2d6", "#6a3d9a"),
    "brown":  ("#ffff99", "#b15928"),
}


def lighten(color, amount=0.5):
    """Lighten a colour by moving it towards white (0 = unchanged, 1 = white).

    Handy for e.g. filled uncertainty bands under a line of the same hue:

    >>> ax.plot(x, y, color=pa.COLORS["blue"])
    >>> ax.fill_between(x, lo, hi, color=pa.lighten(pa.COLORS["blue"], 0.7))
    """
    h, l, s = colorsys.rgb_to_hls(*mcolors.to_rgb(color))
    return colorsys.hls_to_rgb(h, l + (1 - l) * amount, s)


def darken(color, amount=0.5):
    """Darken a colour by moving it towards black (0 = unchanged, 1 = black)."""
    h, l, s = colorsys.rgb_to_hls(*mcolors.to_rgb(color))
    return colorsys.hls_to_rgb(h, l * (1 - amount), s)


# ----------------------------------------------------------------------
# Colour-vision-deficiency simulation
# ----------------------------------------------------------------------

# Machado, Oliveira & Fernandes (2009), IEEE TVCG 15(6) — severity-1.0
# transformation matrices, applied in linear RGB.
_CVD_MATRICES = {
    "protanopia": np.array([
        [0.152286, 1.052583, -0.204868],
        [0.114503, 0.786281, 0.099216],
        [-0.003882, -0.048116, 1.051998]]),
    "deuteranopia": np.array([
        [0.367322, 0.860646, -0.227968],
        [0.280085, 0.672501, 0.047413],
        [-0.011820, 0.042940, 0.968881]]),
    "tritanopia": np.array([
        [1.255528, -0.076749, -0.178779],
        [-0.078411, 0.930809, 0.147602],
        [0.004733, 0.691367, 0.303900]]),
}


def _srgb_to_linear(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _linear_to_srgb(c):
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def simulate_cvd(colors, kind="deuteranopia"):
    """Simulate how colours appear with a colour-vision deficiency.

    Parameters
    ----------
    colors : colour, sequence of colours, or (..., 3/4) float array
        Anything matplotlib understands (hex strings, names, RGB tuples,
        an image array from a rendered figure, ...).
    kind : {"deuteranopia", "protanopia", "tritanopia", "greyscale"}
        Deficiency to simulate. Deuteranopia and protanopia (red-green)
        together affect ~5% of male readers; greyscale is what a
        black-and-white printout shows.

    Returns
    -------
    ndarray of RGB(A) values in [0, 1], one row per input colour (or the
    same shape as an input image array).

    Notes
    -----
    Uses the severity-1.0 matrices of Machado et al. (2009), applied in
    linear RGB — the same model behind most online CVD simulators.
    """
    arr = np.asarray(colors, dtype=float) if (
        isinstance(colors, np.ndarray) and colors.ndim >= 2
    ) else np.atleast_2d(mcolors.to_rgba_array(colors))
    if arr.max() > 1.0:  # e.g. uint8 image content passed as float
        arr = arr / 255.0
    rgb, alpha = arr[..., :3], arr[..., 3:]
    lin = _srgb_to_linear(np.clip(rgb, 0, 1))
    if kind == "greyscale":
        lum = lin @ np.array([0.2126, 0.7152, 0.0722])
        lin = np.repeat(lum[..., None], 3, axis=-1)
    elif kind in _CVD_MATRICES:
        lin = lin @ _CVD_MATRICES[kind].T
    else:
        options = ", ".join(list(_CVD_MATRICES) + ["greyscale"])
        raise ValueError(f"kind must be one of: {options}; got {kind!r}")
    out = _linear_to_srgb(np.clip(lin, 0, 1))
    return np.concatenate([out, alpha], axis=-1) if alpha.size else out


def check_colors(palette=None, kinds=("deuteranopia", "protanopia", "greyscale")):
    """Show a palette next to CVD simulations of it, to verify that the
    colours stay distinguishable. Returns the figure.

    Parameters
    ----------
    palette : dict, list of colours, or None
        Defaults to the package's colour cycle.
    kinds : sequence of str
        Simulations to include (see :func:`simulate_cvd`).
    """
    palette = palette if palette is not None else COLORS
    cols = list(palette.values()) if isinstance(palette, dict) else list(palette)
    rows = ["original", *kinds]
    fig, ax = plt.subplots(
        figsize=figsize("full", journal="mnras", fraction=0.9,
                        height=0.4 * len(rows) + 0.4))
    ax.set_axis_off()
    for i, row in enumerate(rows):
        y = len(rows) - 1 - i
        shown = cols if row == "original" else simulate_cvd(cols, row)
        for j, c in enumerate(shown):
            ax.add_patch(plt.Rectangle((j, y + 0.12), 0.92, 0.76, color=c))
        ax.text(-0.15, y + 0.5, row, ha="right", va="center", fontsize=8)
    ax.set_xlim(-2.2, len(cols))
    ax.set_ylim(0, len(rows))
    ax.set_title("Colour-vision-deficiency check")
    return fig


def check_figure(fig=None, kinds=("deuteranopia", "protanopia", "greyscale")):
    """Render an existing figure and show how it appears under CVD
    simulations — the final accessibility check before submission.

    Parameters
    ----------
    fig : Figure, optional
        Defaults to the current figure.
    kinds : sequence of str
        Simulations to include (see :func:`simulate_cvd`).

    Returns
    -------
    The new comparison figure.
    """
    fig = fig if fig is not None else plt.gcf()
    fig.canvas.draw()
    img = np.asarray(fig.canvas.buffer_rgba(), dtype=float) / 255.0
    panels = [("original", img)] + [(k, simulate_cvd(img, k)) for k in kinds]
    n = len(panels)
    ar = img.shape[0] / img.shape[1]
    w = 6.5
    out, axes = plt.subplots(1, n, figsize=(w, ar * w / n * 1.15))
    for ax, (label, im) in zip(np.atleast_1d(axes), panels):
        ax.imshow(im)
        ax.set_axis_off()
        ax.set_title(label, fontsize=8)
    return out
