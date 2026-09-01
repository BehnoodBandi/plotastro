"""plotastro — publication-quality matplotlib figures for astronomy journals.

One import gives you journal-matched styles, correctly sized figures and a
colour-blind-friendly palette:

    import matplotlib.pyplot as plt
    import plotastro as pa

    pa.set_style("mnras")          # or "aanda", "apj", "oja", "prd", ...
    fig, ax = pa.subplots()        # one-column, golden-ratio figure
    ax.plot(x, y, label="model")
    ax.set_xlabel("$x$")
    ax.legend()
    pa.savefig("myplot")           # -> myplot.pdf

Importing plotastro also registers the styles with matplotlib itself, so
``plt.style.use("mnras")`` works anywhere afterwards.

Supported journals: MNRAS, RASTI, A&A, ApJ/ApJL (AASTeX), the Open Journal
of Astrophysics, PRD/PRL (REVTeX), JCAP and Nature Astronomy — plus
"thesis" and "beamer" width presets. See the README for the full tutorial.
"""

from importlib.metadata import PackageNotFoundError, version as _version

import matplotlib as _mpl
import matplotlib.style as _mstyle

from ._authors import authorlist
from ._core import (
    GOLDEN, JOURNALS, STYLE_DIR,
    current_journal, figsize, savefig, set_size, set_style, subplots, use,
)
from ._colors import (
    COLORS, CYCLE, OKABE_ITO, PAIRED, PETROFF10,
    check_colors, check_figure, darken, lighten, simulate_cvd,
)
from ._extras import (
    LINESTYLES, MARKERS,
    label_panels, show_colors, show_linestyles, show_markers, style_cycler,
)

try:
    __version__ = _version("plotastro")
except PackageNotFoundError:  # running from a source checkout
    __version__ = "0+unknown"

__all__ = [
    "set_style", "use", "figsize", "subplots", "savefig", "current_journal",
    "authorlist",
    "JOURNALS", "GOLDEN", "STYLE_DIR",
    "COLORS", "CYCLE", "OKABE_ITO", "PETROFF10", "PAIRED",
    "lighten", "darken", "simulate_cvd", "check_colors", "check_figure",
    "MARKERS", "LINESTYLES", "style_cycler", "label_panels",
    "show_colors", "show_markers", "show_linestyles",
    "set_size",
]


def _register_styles():
    """Make the bundled styles available as plt.style.use("mnras") etc."""
    for path in STYLE_DIR.glob("*.mplstyle"):
        _mstyle.library[path.stem] = _mpl.rc_params_from_file(
            path, use_default_template=False)
    _mstyle.available[:] = sorted(_mstyle.library)


_register_styles()
