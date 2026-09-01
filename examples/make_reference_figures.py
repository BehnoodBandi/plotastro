"""Generate the reference figures embedded in README.md.

Run from the repository root:  python examples/make_reference_figures.py
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

try:
    import plotastro as pa
except ImportError:  # running from a source checkout without installing
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    import plotastro as pa

FIGDIR = Path(__file__).resolve().parent / "figures"
FIGDIR.mkdir(exist_ok=True)
rng = np.random.default_rng(42)


def save(fig, name):
    fig.savefig(FIGDIR / f"{name}.png", dpi=300)
    plt.close(fig)
    print(f"wrote figures/{name}.png")


# ---------------------------------------------------------------- column plot
pa.set_style("mnras")

x = np.linspace(0.5, 10, 18)
truth = 2.0 * x ** -0.7
y = truth * rng.normal(1, 0.08, x.size)
yerr = 0.08 * truth
xf = np.linspace(0.4, 11, 200)

fig, ax = pa.subplots()
ax.errorbar(x, y, yerr=yerr, fmt="o", color=pa.COLORS["blue"],
            label="mock data", zorder=3)
ax.plot(xf, 2.0 * xf ** -0.7, color=pa.COLORS["red"], label=r"$2\,x^{-0.7}$")
ax.fill_between(xf, 1.8 * xf ** -0.7, 2.2 * xf ** -0.7,
                color=pa.lighten(pa.COLORS["red"], 0.75), zorder=0,
                label=r"$1\sigma$ band")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel(r"$r\ \mathrm{[Mpc]}$")
ax.set_ylabel(r"$\xi(r)$")
ax.legend()
save(fig, "example_column")

# ------------------------------------------------------------ full-width plot
k = np.logspace(-3, 1, 300)
fig, axes = pa.subplots(1, 2, width="full", aspect=0.75)
for i, z in enumerate([0, 0.5, 1, 2]):
    pk = 1e4 * k / (1 + (k / 0.02) ** 2.2) / (1 + z) ** 1.5
    axes[0].loglog(k, pk, label=f"$z={z}$")
    axes[1].semilogx(k, pk / (1e4 * k / (1 + (k / 0.02) ** 2.2)),
                     label=f"$z={z}$")
axes[0].set_xlabel(r"$k\ [h\,\mathrm{Mpc}^{-1}]$")
axes[0].set_ylabel(r"$P(k)\ [h^{-3}\,\mathrm{Mpc}^{3}]$")
axes[1].set_xlabel(r"$k\ [h\,\mathrm{Mpc}^{-1}]$")
axes[1].set_ylabel(r"$P(k)/P(k, z=0)$")
axes[0].legend()
pa.label_panels(axes)
save(fig, "example_full")

# ------------------------------------------------- palette / marker reference
save(pa.show_colors(), "palette")
save(pa.show_colors(pa.OKABE_ITO, title="Okabe & Ito (2008) — plotastro.OKABE_ITO"),
     "palette_okabe_ito")
save(pa.show_markers(), "markers")
save(pa.show_linestyles(), "linestyles")

# ------------------------------------------------------- redundant encoding
x = np.linspace(0, 3, 60)
fig, ax = pa.subplots()
ax.set_prop_cycle(pa.style_cycler(markers=True, linestyles=True))
for n in range(4):
    ax.plot(x, x ** (0.5 + 0.4 * n), markevery=7, label=f"model {n + 1}")
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.legend()
save(fig, "redundant_encoding")

# --------------------------------------------------------------- CVD check
save(pa.check_colors(), "cvd_check")
