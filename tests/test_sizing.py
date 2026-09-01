import pytest

import plotastro as pa

PT = 72.27


def test_column_and_full_widths():
    for key, spec in pa.JOURNALS.items():
        w, h = pa.figsize("column", journal=key)
        assert w == pytest.approx(spec["column"] / PT)
        assert h == pytest.approx(w * pa.GOLDEN)
        w_full, _ = pa.figsize("full", journal=key)
        assert w_full == pytest.approx(spec["full"] / PT)


def test_fraction_points_aspect_height():
    w, h = pa.figsize("column", journal="mnras", fraction=0.5)
    assert w == pytest.approx(120.0 / PT)
    w, h = pa.figsize(345.0)
    assert w == pytest.approx(345.0 / PT)
    w, h = pa.figsize("column", journal="mnras", aspect=1)
    assert h == pytest.approx(w)
    _, h = pa.figsize("column", journal="mnras", height=2.5)
    assert h == 2.5


def test_grid_scaling():
    w1, h1 = pa.figsize("full", journal="mnras", nrows=2, ncols=2)
    w2, h2 = pa.figsize("full", journal="mnras")
    assert w1 == w2 and h1 == pytest.approx(h2)  # 2x2 keeps panel aspect
    _, h3 = pa.figsize("full", journal="mnras", nrows=2, ncols=1)
    assert h3 == pytest.approx(2 * h2)


def test_figsize_defaults_to_current_journal():
    pa.set_style("aanda")
    w, _ = pa.figsize("column")
    assert w == pytest.approx(pa.JOURNALS["aanda"]["column"] / PT)


def test_bad_width_string_raises():
    with pytest.raises(ValueError, match="column"):
        pa.figsize("enormous")


def test_subplots_returns_correct_size():
    pa.set_style("mnras")
    fig, axes = pa.subplots(2, 3, width="full", sharex=True)
    assert axes.shape == (2, 3)
    expected = pa.figsize("full", nrows=2, ncols=3)
    assert tuple(fig.get_size_inches()) == pytest.approx(expected)


def test_legacy_set_size():
    assert pa.set_size("mnras") == pa.figsize("column", journal="mnras")
    assert pa.set_size("mnras_full") == pa.figsize("full", journal="mnras")
    assert pa.set_size(300.0)[0] == pytest.approx(300.0 / PT)
    # the old hight_ratio typo still works
    _, h = pa.set_size("mnras", hight_ratio=2)
    assert h == pytest.approx(2 * pa.set_size("mnras")[1])


def test_savefig_multiple_formats(tmp_path):
    pa.set_style("mnras")
    fig, ax = pa.subplots()
    ax.plot([0, 1], [0, 1])
    written = pa.savefig(tmp_path / "fig", fig=fig, formats=("pdf", "png"))
    assert [w.endswith(("fig.pdf", "fig.png")) for w in written] == [True, True]
    for w in written:
        assert (tmp_path / w.split("/")[-1]).stat().st_size > 0
    # explicit extension selects that single format
    written = pa.savefig(tmp_path / "other.png", fig=fig)
    assert written[0].endswith("other.png")
