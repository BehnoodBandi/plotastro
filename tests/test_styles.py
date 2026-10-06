import matplotlib.pyplot as plt
import pytest

import plotastro as pa

JOURNAL_STYLES = ["mnras", "rasti", "aanda", "apj", "oja", "prd", "jcap", "natastro",
                  "euclid"]


def test_all_style_files_exist():
    for key in JOURNAL_STYLES:
        assert (pa.STYLE_DIR / f"{key}.mplstyle").is_file()


def test_styles_registered_with_matplotlib():
    # `import plotastro` should make plt.style.use("mnras") work directly.
    for key in JOURNAL_STYLES:
        assert key in plt.style.available
        plt.style.use(key)


@pytest.mark.parametrize("key", JOURNAL_STYLES)
def test_set_style_applies_expected_params(key):
    pa.set_style(key)
    assert pa.current_journal() == key
    assert len(plt.rcParams["axes.prop_cycle"]) == (8 if key == "euclid" else 12)
    assert plt.rcParams["savefig.format"] == "pdf"
    assert plt.rcParams["pdf.fonttype"] == 42
    assert plt.rcParams["text.usetex"] is False
    # default figsize must be the journal's column width
    expected_w = pa.JOURNALS[key]["column"] / 72.27
    assert plt.rcParams["figure.figsize"][0] == pytest.approx(expected_w)


def test_natastro_is_sans_serif():
    pa.set_style("natastro")
    assert plt.rcParams["font.family"] == ["sans-serif"]
    assert plt.rcParams["font.size"] == 7
    pa.set_style("mnras")
    assert plt.rcParams["font.family"] == ["serif"]
    assert plt.rcParams["font.size"] == 9


def test_aliases_and_presets():
    for alias, key in [("a&a", "aanda"), ("apjl", "apj"), ("nature", "natastro"),
                       ("prl", "prd"), ("A&A", "aanda"), ("ec", "euclid")]:
        pa.set_style(alias)
        assert pa.current_journal() == key
    # thesis/beamer share the mnras style file but get their own width
    pa.set_style("thesis")
    assert plt.rcParams["figure.figsize"][0] == pytest.approx(426.79135 / 72.27)


def test_unknown_journal_raises():
    with pytest.raises(ValueError, match="Unknown journal"):
        pa.set_style("nope")


def test_overrides():
    pa.set_style("mnras", grid=False, **{"font.size": 11})
    assert plt.rcParams["axes.grid"] is False
    assert plt.rcParams["font.size"] == 11


def test_usetex_flag():
    pa.set_style("mnras", usetex=True)
    assert plt.rcParams["text.usetex"] is True
    assert "newtx" in plt.rcParams["text.latex.preamble"]
    pa.set_style("natastro", usetex=True)
    assert "helvet" in plt.rcParams["text.latex.preamble"]
    pa.set_style("euclid", usetex=True)   # niceplots: plain LaTeX, no preamble
    assert plt.rcParams["text.usetex"] is True
    assert plt.rcParams["text.latex.preamble"] == ""


def test_euclid_follows_niceplots():
    pa.set_style("euclid")
    rc = plt.rcParams
    assert rc["font.family"] == ["sans-serif"]
    assert rc["font.size"] == 10
    assert rc["mathtext.fontset"] == "cm"
    assert tuple(rc["figure.figsize"]) == pytest.approx((4.0, 3.0))
    assert rc["axes.grid"] is False
    assert rc["xtick.minor.visible"] is False
    assert rc["legend.frameon"] is True
    assert rc["lines.linewidth"] == 1.0
    assert rc["lines.markersize"] == 5.0
    assert rc["xtick.major.size"] == 2.5
    assert rc["xtick.major.pad"] == 5.0
    assert rc["axes.xmargin"] == 0
    cycle = [c["color"].lower() for c in rc["axes.prop_cycle"]]
    assert cycle == list(pa.PETROFF8.values())
    # niceplots' sizing convention: 4 x 3 in, two columns = twice that
    assert pa.figsize("full", journal="euclid") == pytest.approx((8.0, 6.0))
    assert pa.figsize("column", journal="euclid", aspect=1) == pytest.approx((4.0, 4.0))
    # the other styles keep the golden ratio
    assert pa.figsize("column", journal="mnras")[1] == pytest.approx(
        240.0 / 72.27 * pa.GOLDEN)
    # switching back must undo everything the Euclid style changed
    pa.set_style("mnras")
    assert plt.rcParams["axes.grid"] is True
    assert plt.rcParams["xtick.minor.visible"] is True
    assert plt.rcParams["legend.frameon"] is True
    assert plt.rcParams["legend.framealpha"] == pytest.approx(0.7)
    assert plt.rcParams["font.family"] == ["serif"]
    assert plt.rcParams["axes.xmargin"] == pytest.approx(0.03)


def test_palette_option():
    pa.set_style("euclid", palette="categorical3")
    cycle = [c["color"].lower() for c in plt.rcParams["axes.prop_cycle"]]
    assert cycle == ["#000000", *pa.TOL_VIBRANT.values()]
    pa.set_style("mnras", palette="okabe_ito")
    cycle = [c["color"].lower() for c in plt.rcParams["axes.prop_cycle"]]
    assert cycle == list(pa.OKABE_ITO.values())
    pa.set_style("mnras", palette=pa.PETROFF8)              # a dict
    assert len(plt.rcParams["axes.prop_cycle"]) == 8
    pa.set_style("mnras", palette=["#123456", "#abcdef"])   # a list
    assert len(plt.rcParams["axes.prop_cycle"]) == 2
    pa.set_style("mnras", palette="diverging")              # niceplots name
    assert len(plt.rcParams["axes.prop_cycle"]) == 8
    with pytest.raises(ValueError, match="Unknown palette"):
        pa.set_style("mnras", palette="rainbow")
    with pytest.raises(ValueError, match="at least one colour"):
        pa.set_style("mnras", palette=[])


def test_all_styles_set_the_same_params():
    """Matplotlib only overwrites the rcParams a style names, so every style
    must name the same ones, or switching styles leaks settings."""
    keys = {key: set(plt.style.library[key]) for key in JOURNAL_STYLES}
    reference = keys["mnras"]
    for key, names in keys.items():
        assert names == reference, (key, names ^ reference)


@pytest.mark.parametrize("before", JOURNAL_STYLES)
@pytest.mark.parametrize("after", ["mnras", "natastro", "euclid"])
def test_switching_styles_is_clean(before, after):
    import matplotlib as mpl
    pa.set_style(after)
    fresh = dict(mpl.rcParams)
    pa.set_style(before)
    pa.set_style(after)
    assert dict(mpl.rcParams) == fresh


@pytest.mark.parametrize("key", [k for k in JOURNAL_STYLES if k != "euclid"])
def test_legend_has_translucent_white_background(key):
    import matplotlib.colors as mcolors
    pa.set_style(key)
    rc = plt.rcParams
    assert rc["legend.frameon"] is True
    assert mcolors.to_rgb(rc["legend.facecolor"]) == (1.0, 1.0, 1.0)
    assert rc["legend.framealpha"] == pytest.approx(0.7)
    assert rc["legend.edgecolor"] == "none"
    # and the drawn legend really gets that background
    fig, ax = plt.subplots()
    ax.plot([0, 1], label="line")
    frame = ax.legend().get_frame()
    assert frame.get_facecolor() == pytest.approx((1.0, 1.0, 1.0, 0.7))
