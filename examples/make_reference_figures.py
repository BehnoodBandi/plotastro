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

# ------------------------------------------- CMasher colours (optional extra)
try:
    import cmasher  # noqa: F401  (only to check it is installed)
except ImportError:
    print("cmasher not installed: skipping figures/cmasher.png")
else:
    pa.set_style("mnras", palette="cmr.rainforest", cmap="cmr.ocean")
    fig, axes = pa.subplots(1, 2, width="full", aspect=0.75)
    x = np.linspace(0, 1, 200)
    for n in range(8):                       # the 8-colour CMasher cycle
        axes[0].plot(x, x ** (0.4 + 0.3 * n), label=f"$n={n + 1}$")
    axes[0].set_xlabel("$x$")
    axes[0].set_ylabel("$x^{\\alpha_n}$")
    axes[0].set_title("palette='cmr.rainforest'", family="monospace", fontsize=8)
    axes[0].legend(ncol=2, fontsize=6)
    yy, xx = np.mgrid[-3:3:200j, -3:3:200j]
    field = (np.exp(-((xx - 0.8) ** 2 + yy ** 2)) + 0.6 * np.exp(
        -((xx + 1.2) ** 2 + (yy - 1) ** 2) / 0.5))
    im = axes[1].imshow(field, origin="lower", extent=(-3, 3, -3, 3))
    axes[1].grid(False)
    axes[1].set_xlabel("$x$")
    axes[1].set_ylabel("$y$")
    axes[1].set_title("cmap='cmr.ocean'", family="monospace", fontsize=8)
    fig.colorbar(im, ax=axes[1], label="density")
    pa.label_panels(axes, loc="lower right")[1].set_color("white")
    save(fig, "cmasher")

    # ------------------------- which CMasher map for which job (overview)
    # Each strip: the map on top, what it becomes in greyscale print below.
    pa.set_style("mnras")
    groups = {
        "Sequential, many hues\n(distinct lines, images)":
            ["rainforest", "torch", "chroma", "neon", "apple"],
        "Sequential, one hue\n(steps of one quantity)":
            ["ocean", "flamingo", "freeze", "jungle", "gothic"],
        "Diverging, white centre\n(signed data, print)":
            ["fusion", "waterlily", "viola", "holly", "prinsenvlag"],
        "Diverging, black centre\n(signed data, dark slides)":
            ["iceburn", "redshift", "wildfire", "seaweed", "watermelon"],
        "Cyclic\n(angles, phases)":
            ["infinity", "seasons", "emergency", "copper"],
    }
    gradient = np.linspace(0, 1, 256)[None, :]
    fig = plt.figure(figsize=pa.figsize("full", aspect=0.45))
    for subfig, (title, names) in zip(fig.subfigures(1, len(groups)),
                                      groups.items()):
        subfig.suptitle(title, fontsize=6.5)
        axes = subfig.subplots(5, 1)
        for ax in axes:
            ax.set_axis_off()
        for ax, name in zip(axes, names):
            rgba = pa.cmasher_cmap(name)(gradient)
            grey = pa.simulate_cvd(rgba, "greyscale")
            ax.imshow(np.vstack([rgba[..., :3]] * 2 + [grey[..., :3]]),
                      aspect="auto")
            ax.set_title(f"cmr.{name}", fontsize=6, family="monospace",
                         pad=1.5)
    save(fig, "cmasher_maps")

    # ------------------------------------- CMasher examples (2 x 2 gallery)
    fig, axes = pa.subplots(2, 2, width="full", aspect=0.8)
    (ax_lines, ax_scatter), (ax_res, ax_phase) = axes

    # (a) many lines coloured by a continuous parameter, with a colour bar
    zs = np.linspace(0, 3, 13)
    cmap = pa.cmasher_cmap("ocean", cmap_range=(0.15, 0.85))
    norm = matplotlib.colors.Normalize(zs.min(), zs.max())
    k = np.logspace(-3, 1, 300)
    for z in zs:
        ax_lines.loglog(k, 1e4 * k / (1 + (k / 0.02) ** 2.2) / (1 + z) ** 1.5,
                        color=cmap(norm(z)))
    fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap),
                 ax=ax_lines, label="$z$")
    ax_lines.set_xlabel(r"$k\ [h\,\mathrm{Mpc}^{-1}]$")
    ax_lines.set_ylabel(r"$P(k)\ [h^{-3}\,\mathrm{Mpc}^{3}]$")
    ax_lines.set_title('cmasher_cmap("ocean", cmap_range=(0.15, 0.85))',
                       family="monospace", fontsize=6)

    # (b) points coloured by a third quantity
    logm = rng.uniform(9, 11.5, 600)
    metal = 0.3 * (logm - 10.2) + rng.normal(0, 0.12, logm.size)
    sfr = 0.8 * (logm - 10) + 0.4 * metal + rng.normal(0, 0.25, logm.size)
    sc = ax_scatter.scatter(logm, sfr, c=metal, s=4, linewidths=0,
                            cmap=pa.cmasher_cmap("rainforest",
                                                 cmap_range=(0.0, 0.85)))
    fig.colorbar(sc, ax=ax_scatter, label=r"$[\mathrm{Fe/H}]$")
    ax_scatter.set_ylim(-2.4, None)          # room for the panel label
    ax_scatter.set_xlabel(r"$\log(M_\star/\mathrm{M_\odot})$")
    ax_scatter.set_ylabel(r"$\log(\mathrm{SFR}/\mathrm{M_\odot\,yr^{-1}})$")
    ax_scatter.set_title('cmasher_cmap("rainforest", cmap_range=(0, 0.85))',
                         family="monospace", fontsize=6)

    # (c) a signed field (residuals) on a diverging map, centred on zero
    yy, xx = np.mgrid[-3:3:150j, -3:3:150j]
    residual = (0.5 * np.exp(-((xx - 1) ** 2 + (yy - 0.5) ** 2) / 0.6)
                - 0.4 * np.exp(-((xx + 1.2) ** 2 + (yy + 1) ** 2) / 0.4)
                + rng.normal(0, 0.05, xx.shape))
    vmax = np.abs(residual).max()
    im = ax_res.imshow(residual, origin="lower", extent=(-3, 3, -3, 3),
                       cmap=pa.cmasher_cmap("fusion"), vmin=-vmax, vmax=vmax)
    fig.colorbar(im, ax=ax_res, label="data $-$ model")
    ax_res.set_title('cmasher_cmap("fusion"), vmin=-vmax, vmax=vmax',
                     family="monospace", fontsize=6)

    # (d) an angle on a cyclic map: -180 and +180 deg get the same colour
    zz = xx + 1j * yy
    phase = np.degrees(np.angle((zz - (1 + 0.5j)) / (zz + (1 + 0.5j))))
    im = ax_phase.imshow(phase, origin="lower", extent=(-3, 3, -3, 3),
                         cmap=pa.cmasher_cmap("infinity"), vmin=-180, vmax=180)
    fig.colorbar(im, ax=ax_phase, label="phase [deg]",
                 ticks=[-180, -90, 0, 90, 180])
    ax_phase.set_title('cmasher_cmap("infinity"), vmin=-180, vmax=180',
                       family="monospace", fontsize=6)

    for ax in (ax_res, ax_phase):
        ax.grid(False)
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
    pa.label_panels(axes, loc="lower left")
    save(fig, "cmasher_examples")
