import matplotlib.colors as mcolors
import numpy as np
import pytest

import plotastro as pa


def test_palettes_are_valid_hex():
    for palette in (pa.COLORS, pa.OKABE_ITO, pa.PETROFF8, pa.PETROFF10,
                    pa.TOL_VIBRANT):
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


def test_euclid_colors():
    assert pa.euclid_colors() == list(pa.PETROFF8.values())
    assert pa.euclid_colors("categorical1") == list(pa.PETROFF8.values())
    assert pa.euclid_colors("categorical2") == list(pa.OKABE_ITO.values())
    assert pa.euclid_colors("categorical3") == ["#000000", *pa.TOL_VIBRANT.values()]
    assert pa.euclid_colors("Categorical-3") == pa.euclid_colors("categorical3")
    seq = pa.euclid_colors("sequential", n=5)
    assert len(seq) == 5
    for c in seq:
        mcolors.to_rgb(c)
    assert len(pa.euclid_colors("diverging", n=3)) == 3
    with pytest.raises(ValueError, match="Unknown Euclid colour scheme"):
        pa.euclid_colors("categorical4")
    with pytest.raises(ValueError, match="positive"):
        pa.euclid_colors("sequential", n=0)


# ----------------------------------------------------------------------
# CMasher (optional dependency)
# ----------------------------------------------------------------------

def test_import_does_not_need_cmasher():
    """plotastro must import and style figures with CMasher unavailable."""
    import os
    import subprocess
    import sys
    from pathlib import Path

    code = (
        "import sys; sys.modules['cmasher'] = None\n"
        "import matplotlib; matplotlib.use('Agg')\n"
        "import plotastro as pa\n"
        "pa.set_style('mnras', palette='okabe_ito', cmap='magma')\n"
    )
    env = dict(os.environ)
    src = str(Path(pa.__file__).resolve().parents[1])
    env["PYTHONPATH"] = os.pathsep.join(filter(None, [src, env.get("PYTHONPATH")]))
    subprocess.run([sys.executable, "-c", code], check=True, env=env)


def test_cmasher_missing_gives_helpful_error(monkeypatch):
    import sys
    import matplotlib.pyplot as plt
    monkeypatch.setitem(sys.modules, "cmasher", None)  # makes `import cmasher` fail
    pa.set_style("mnras", palette="okabe_ito")
    before = dict(plt.rcParams)
    for call in (lambda: pa.cmasher_colors("rainforest"),
                 lambda: pa.cmasher_cmap("rainforest"),
                 lambda: pa.set_style("euclid", palette="cmr.rainforest"),
                 lambda: pa.set_style("euclid", cmap="cmr.rainforest")):
        with pytest.raises(ImportError, match="pip install cmasher"):
            call()
    # the failed set_style calls left the active style alone
    assert pa.current_journal() == "mnras"
    assert dict(plt.rcParams) == before


def test_set_style_cmap_without_cmasher():
    import matplotlib.pyplot as plt
    pa.set_style("mnras", cmap="cividis")
    assert plt.rcParams["image.cmap"] == "cividis"
    pa.set_style("mnras")
    assert plt.rcParams["image.cmap"] == "viridis"
    with pytest.raises(ValueError, match="Unknown colormap"):
        pa.set_style("mnras", cmap="no_such_map")


def test_cmasher_colors():
    cmr = pytest.importorskip("cmasher")
    cols = pa.cmasher_colors("rainforest")
    assert len(cols) == 8
    for c in cols:
        mcolors.to_rgb(c)
    assert pa.cmasher_colors("cmr.rainforest", 5) == pa.cmasher_colors("rainforest", n=5)
    assert pa.cmasher_colors(cmr.rainforest, 5) == pa.cmasher_colors("rainforest", 5)
    expected = cmr.take_cmap_colors("cmr.torch", 4, cmap_range=(0.2, 0.9),
                                    return_fmt="hex")
    assert pa.cmasher_colors("torch", 4, cmap_range=(0.2, 0.9)) == \
        [c.lower() for c in expected]
    # the default range drops the black and white ends
    assert "#000000" not in cols and "#ffffff" not in cols
    assert pa.cmasher_colors("rainforest", 2, cmap_range=(0, 1)) == ["#000000", "#ffffff"]
    with pytest.raises(ValueError, match="positive"):
        pa.cmasher_colors("rainforest", n=0)
    with pytest.raises(ValueError, match="Unknown CMasher colormap"):
        pa.cmasher_colors("viridis")


def test_cmasher_cmap():
    pytest.importorskip("cmasher")
    cmap = pa.cmasher_cmap("iceburn")
    assert isinstance(cmap, mcolors.Colormap)
    assert cmap.name == "cmr.iceburn"
    assert pa.cmasher_cmap("cmr.ocean_r").name == "cmr.ocean_r"
    assert pa.cmasher_cmap("iceburn", n=6).N == 6
    sub = pa.cmasher_cmap("rainforest", cmap_range=(0.15, 0.85))
    assert 0 < sub.N < cmap.N
    assert mcolors.to_hex(sub(0.0)) != "#000000"
    with pytest.raises(ValueError, match="Unknown CMasher colormap"):
        pa.cmasher_cmap("no_such_map")


def test_set_style_with_cmasher():
    import matplotlib.pyplot as plt
    pytest.importorskip("cmasher")
    pa.set_style("mnras", palette="cmr.rainforest", cmap="cmr.ocean")
    style_colors = [c["color"] for c in plt.rcParams["axes.prop_cycle"]]
    assert style_colors == pa.cmasher_colors("rainforest")
    assert plt.rcParams["image.cmap"] == "cmr.ocean"
    fig, ax = plt.subplots()
    assert ax.imshow([[0, 1], [2, 3]]).get_cmap().name == "cmr.ocean"
    with pytest.raises(ValueError, match="Unknown CMasher colormap"):
        pa.set_style("mnras", palette="cmr.no_such_map")
