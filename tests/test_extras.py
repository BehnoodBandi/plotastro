import pytest

import plotastro as pa


def test_style_cycler_defaults():
    c = pa.style_cycler()
    assert len(c) == 12
    assert set(c.keys) == {"color"}


def test_style_cycler_combined():
    c = pa.style_cycler(markers=True, linestyles=True)
    assert len(c) == 8
    assert set(c.keys) == {"color", "marker", "linestyle"}
    c = pa.style_cycler(n=20, markers=True)  # wraps past sequence lengths
    assert len(c) == 20


def test_style_cycler_empty_raises():
    with pytest.raises(ValueError):
        pa.style_cycler(colors=False)


def test_label_panels_grid():
    pa.set_style("mnras")
    fig, axes = pa.subplots(2, 2)
    texts = pa.label_panels(axes)
    assert [t.get_text() for t in texts] == ["(a)", "(b)", "(c)", "(d)"]


def test_label_panels_options():
    fig, ax = pa.subplots()
    (t,) = pa.label_panels(ax, fmt="{}", uppercase=True, loc="outside",
                           fontweight="bold")
    assert t.get_text() == "A"
    assert t.get_fontweight() == "bold"
    (t2,) = pa.label_panels(ax, labels=["(iv)"], loc="lower right")
    assert t2.get_text() == "(iv)"
    with pytest.raises(ValueError, match="loc must be"):
        pa.label_panels(ax, loc="middle")


def test_reference_charts_return_figures():
    for fig in (pa.show_colors(), pa.show_colors(pa.PETROFF10),
                pa.show_markers(), pa.show_linestyles()):
        assert fig is not None


def test_linestyles_are_usable():
    fig, ax = pa.subplots()
    for ls in pa.LINESTYLES.values():
        ax.plot([0, 1], [0, 1], ls=ls)
    for m in pa.MARKERS:
        ax.plot([0.5], [0.5], marker=m)
