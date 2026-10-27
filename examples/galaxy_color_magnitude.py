"""Example galaxy colour-magnitude diagram using plotastro.

The red sequence and blue cloud here are illustrative *synthetic* samples,
not observed galaxies or fits to survey data.

Run from the repository root:
    python examples/galaxy_color_magnitude.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import plotastro as pa


def main() -> None:
    rng = np.random.default_rng(42)

    # Simulated SDSS-like absolute r-band magnitudes and g-r colours.
    m_blue = np.clip(rng.normal(-19.7, 1.15, 650), -23.3, -16.8)
    m_red = np.clip(rng.normal(-21.0, 0.90, 400), -23.3, -16.8)

    blue_color = 0.47 - 0.035 * (m_blue + 20) + rng.normal(0, 0.13, m_blue.size)
    red_color = 0.79 - 0.025 * (m_red + 20) + rng.normal(0, 0.07, m_red.size)

    pa.set_style("mnras")
    fig, ax = pa.subplots()
    ax.scatter(
        m_blue, blue_color, s=8, alpha=0.55, color=pa.COLORS["blue"],
        edgecolors="none", rasterized=True, label="Blue cloud (mock)",
    )
    ax.scatter(
        m_red, red_color, s=8, alpha=0.55, color=pa.COLORS["red"],
        edgecolors="none", rasterized=True, label="Red sequence (mock)",
    )

    ax.set_xlabel(r"Absolute magnitude $M_r$ (mag)")
    ax.set_ylabel(r"Rest-frame colour $(g-r)$ (mag)")
    ax.set_xlim(-23.5, -16.5)
    ax.set_ylim(0.0, 1.2)
    ax.legend(loc="upper right", fontsize=7)

    output = Path(__file__).resolve().parent / "figures" / "galaxy_color_magnitude.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
