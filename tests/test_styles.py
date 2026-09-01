import matplotlib.pyplot as plt
import pytest

import plotastro as pa

JOURNAL_STYLES = ["mnras", "rasti", "aanda", "apj", "oja", "prd", "jcap", "natastro"]


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
    assert len(plt.rcParams["axes.prop_cycle"]) == 12
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
                       ("prl", "prd"), ("A&A", "aanda")]:
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
