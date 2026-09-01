import matplotlib.colors as mcolors
import numpy as np
import pytest

import plotastro as pa


def test_palettes_are_valid_hex():
    for palette in (pa.COLORS, pa.OKABE_ITO, pa.PETROFF10):
        for c in palette.values():
            mcolors.to_rgb(c)  # raises on invalid colours
    for light, dark in pa.PAIRED.values():
        mcolors.to_rgb(light)
        mcolors.to_rgb(dark)


def test_cycle_matches_style():
    import matplotlib.pyplot as plt
    pa.set_style("mnras")
    style_colors = [c["color"] for c in plt.rcParams["axes.prop_cycle"]]
    assert [c.lower() for c in style_colors] == list(pa.COLORS.values())


def test_lighten_darken():
    c = pa.COLORS["blue"]
    assert pa.lighten(c, 0) == pytest.approx(mcolors.to_rgb(c))
    assert pa.lighten(c, 1) == pytest.approx((1, 1, 1))
    assert pa.darken(c, 1) == pytest.approx((0, 0, 0))
    lighter = pa.lighten(c, 0.5)
    assert all(l >= o for l, o in zip(lighter, mcolors.to_rgb(c)))


def test_simulate_cvd_shapes_and_range():
    out = pa.simulate_cvd(list(pa.COLORS.values()), "deuteranopia")
    assert out.shape == (12, 4)
    assert out.min() >= 0 and out.max() <= 1
    # single colour
    out = pa.simulate_cvd("#377eb8", "protanopia")
    assert out.shape == (1, 4)
    # image array
    img = np.random.default_rng(0).random((5, 7, 3))
    out = pa.simulate_cvd(img, "tritanopia")
    assert out.shape == (5, 7, 3)


def test_simulate_greyscale_is_grey():
    out = pa.simulate_cvd(["#e41a1c", "#4daf4a"], "greyscale")
    for row in out:
        assert row[0] == pytest.approx(row[1]) == pytest.approx(row[2])


def test_simulate_cvd_bad_kind():
    with pytest.raises(ValueError, match="kind must be"):
        pa.simulate_cvd("#000000", "monet")


def test_check_colors_and_figure():
    import matplotlib.pyplot as plt
    fig = pa.check_colors()
    assert fig is not None
    src, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    out = pa.check_figure(src)
    assert len(out.axes) == 4  # original + 3 simulations
