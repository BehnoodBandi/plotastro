"""Journal definitions, style activation and figure sizing."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

STYLE_DIR = Path(__file__).resolve().parent / "styles"

#: Golden ratio (height/width) used for default figure heights.
GOLDEN = (5 ** 0.5 - 1) / 2  # 0.618...

_SERIF_TEX = r"\usepackage{newtxtext}\usepackage{newtxmath}"
_SANS_TEX = (r"\usepackage{helvet}\usepackage{sansmath}\sansmath"
             r"\renewcommand{\familydefault}{\sfdefault}")

#: Text-block widths in LaTeX points (1 pt = 1/72.27 inch) per journal,
#: the style sheet each journal uses, and its LaTeX font preamble.
JOURNALS = {
    "mnras":    {"column": 240.0,     "full": 504.0,     "style": "mnras",
                 "tex": _SERIF_TEX,
                 "name": "Monthly Notices of the RAS"},
    "rasti":    {"column": 240.0,     "full": 504.0,     "style": "rasti",
                 "tex": _SERIF_TEX,
                 "name": "RAS Techniques and Instruments"},
    "aanda":    {"column": 250.38,    "full": 512.15,    "style": "aanda",
                 "tex": _SERIF_TEX,
                 "name": "Astronomy & Astrophysics"},
    "apj":      {"column": 242.26653, "full": 513.11743, "style": "apj",
                 "tex": _SERIF_TEX,
                 "name": "The Astrophysical Journal (AASTeX)"},
    "oja":      {"column": 245.26653, "full": 508.0,     "style": "oja",
                 "tex": _SERIF_TEX,
                 "name": "The Open Journal of Astrophysics"},
    "prd":      {"column": 246.0,     "full": 510.0,     "style": "prd",
                 "tex": _SERIF_TEX,
                 "name": "Physical Review D (REVTeX 4.2)"},
    "jcap":     {"column": 455.24,    "full": 455.24,    "style": "jcap",
                 "tex": _SERIF_TEX,
                 "name": "J. of Cosmology and Astroparticle Physics"},
    "natastro": {"column": 253.23,    "full": 520.68,    "style": "natastro",
                 "tex": _SANS_TEX,
                 "name": "Nature Astronomy"},
    # Not journals, but handy width presets (they use the MNRAS look):
    "thesis":   {"column": 426.79135, "full": 426.79135, "style": "mnras",
                 "tex": _SERIF_TEX,
                 "name": "A4 thesis text width"},
    "beamer":   {"column": 307.28987, "full": 307.28987, "style": "mnras",
                 "tex": _SERIF_TEX,
                 "name": "Beamer slide text width"},
}

_ALIASES = {
    "a&a": "aanda", "aa": "aanda", "astronomy&astrophysics": "aanda",
    "apjl": "apj", "aj": "apj", "aas": "apj", "aastex": "apj",
    "openjournal": "oja", "theoj": "oja", "openjournalofastrophysics": "oja",
    "prl": "prd", "aps": "prd", "revtex": "prd",
    "nature": "natastro", "natureastronomy": "natastro", "natastron": "natastro",
    "mnras_full": "mnras",  # legacy name from the old set_size() API
}

_state = {"journal": "mnras"}


def _resolve(journal):
    key = str(journal).lower().replace(" ", "").replace("-", "")
    key = _ALIASES.get(key, key)
    if key not in JOURNALS:
        options = ", ".join(sorted(JOURNALS))
        raise ValueError(f"Unknown journal {journal!r}. Choose one of: {options}")
    return key


def current_journal():
    """Name of the journal activated by the last :func:`set_style` call."""
    return _state["journal"]


# ----------------------------------------------------------------------
# Style activation
# ----------------------------------------------------------------------

def set_style(journal="mnras", *, usetex=False, grid=None, **rc_overrides):
    """Activate the plotting style for a journal.

    Parameters
    ----------
    journal : str
        One of ``"mnras"``, ``"rasti"``, ``"aanda"`` (aliases ``"a&a"``,
        ``"aa"``), ``"apj"`` (aliases ``"apjl"``, ``"aastex"``), ``"oja"``,
        ``"prd"`` (aliases ``"prl"``, ``"revtex"``), ``"jcap"``,
        ``"natastro"`` (alias ``"nature"``), ``"thesis"`` or ``"beamer"``.
    usetex : bool, optional
        If True, render all text with a real LaTeX installation using
        fonts matching the journal (newtx Times for the serif journals,
        Helvetica for Nature Astronomy). Default False (portable mathtext).
    grid : bool, optional
        Override the style's grid setting (the styles default to a
        subtle grid; pass ``grid=False`` for a clean journal look).
    **rc_overrides
        Any extra rcParams, e.g. ``set_style("mnras", **{"font.size": 10})``.

    Examples
    --------
    >>> pa.set_style("aanda")
    >>> pa.set_style("mnras", usetex=True, grid=False)
    """
    key = _resolve(journal)
    style_file = STYLE_DIR / f"{JOURNALS[key]['style']}.mplstyle"
    plt.style.use(style_file)
    _state["journal"] = key
    # Presets sharing a style file (thesis, beamer) still get the right
    # default figure size:
    mpl.rcParams["figure.figsize"] = figsize("column", journal=key)
    if usetex:
        mpl.rcParams.update({
            "text.usetex": True,
            "text.latex.preamble": JOURNALS[key]["tex"],
        })
    if grid is not None:
        mpl.rcParams["axes.grid"] = bool(grid)
    if rc_overrides:
        mpl.rcParams.update(rc_overrides)


#: Alias for :func:`set_style`, for those who prefer ``pa.use("mnras")`` —
#: after which everything is plain matplotlib.
use = set_style


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
    >>> fig, ax = pa.subplots()                          # one-column figure
    >>> fig, axes = pa.subplots(2, 2, width="full")      # full-width 2x2 grid
    >>> fig, ax = pa.subplots(aspect=1)                  # square panel
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
