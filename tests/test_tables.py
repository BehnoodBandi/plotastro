import numpy as np
import pytest

import plotastro as pa

DATA = {
    "name": ["NGC_1300", "M31"],
    "z": [0.0052, 1.23456],
    "z_lo": [0.0003, 0.012],
    "z_hi": [0.0004, 0.034],
    "mass": [10.523, 11.2],
    "mass_err": [0.123, 0.05],
}


def flat(tex):
    """tex with the column padding collapsed to single spaces."""
    return " ".join(tex.split())


def body(tex):
    """The table rows between the header rule and the closing rule."""
    lines = [flat(line) for line in tex.splitlines()]
    rules = [i for i, line in enumerate(lines)
             if line in (r"\hline", r"\midrule", r"\bottomrule")]
    return lines[rules[-2] + 1:rules[-1]]


def test_mnras_layout():
    tex = pa.latex_table({"a": [1.5, 2.25]}, caption="Cap.", label="tab:x")
    lines = [line.strip() for line in tex.splitlines()]
    assert lines[:5] == [r"\begin{table}", r"\centering", r"\caption{Cap.}",
                         r"\label{tab:x}", r"\begin{tabular}{c}"]
    assert lines[5:] == [r"\hline", r"a \\", r"\hline", r"1.50 \\",
                         r"2.25 \\", r"\hline", r"\end{tabular}",
                         r"\end{table}"]


def test_errors_folded_into_columns():
    tex = pa.latex_table(DATA, errors={"z": ("z_lo", "z_hi"),
                                       "mass": "mass_err"})
    assert r"name & z & mass \\" in flat(tex)          # error cols gone
    rows = body(tex)
    # the error sets the precision: 2 significant figures by default
    assert rows[0].startswith(r"NGC\_1300")
    assert r"$0.00520^{+0.00040}_{-0.00030}$" in rows[0]
    assert r"$10.52 \pm 0.12$" in rows[0]
    assert r"$1.235^{+0.034}_{-0.012}$" in rows[1]
    assert r"$11.200 \pm 0.050$" in rows[1]


def test_equal_asymmetric_errors_become_pm():
    tex = pa.latex_table({"x": [1.0], "lo": [0.1], "hi": [0.1]},
                         errors={"x": ("lo", "hi")})
    assert r"$1.00 \pm 0.10$" in tex


def test_negative_lower_errors_accepted():
    tex = pa.latex_table({"x": [1.0], "lo": [-0.1], "hi": [0.2]},
                         errors={"x": ["lo", "hi"]})
    assert r"$1.00^{+0.20}_{-0.10}$" in tex


def test_missing_error_formats_plain_value():
    tex = pa.latex_table({"x": [9.87654, 1.0], "e": [np.nan, 0.0]},
                         errors={"x": "e"})
    assert body(tex) == [r"9.88 \\", r"1.00 \\"]


def test_sig_per_column():
    tex = pa.latex_table({"a": [1.23456], "b": [1.23456], "c": [0.0012345]},
                         sig={"a": 2, "b": 5})
    assert body(tex) == [r"1.2 & 1.2346 & 0.00123 \\"]
    tex = pa.latex_table({"a": [12345.0], "b": [9.96]}, sig=2)
    assert body(tex) == [r"12000 & 10 \\"]


def test_sig_on_error_column():
    tex = pa.latex_table(DATA, columns=["mass"], errors={"mass": "mass_err"},
                         sig=1)
    assert body(tex) == [r"$10.5 \pm 0.1$ \\", r"$11.20 \pm 0.05$ \\"]


def test_decimals():
    tex = pa.latex_table({"a": [3.14159, 2.0], "b": [-0.0001, 7.0]},
                         decimals={"a": 3, "b": 1})
    assert body(tex) == [r"3.142 & 0.0 \\", r"2.000 & 7.0 \\"]   # no "-0.0"
    tex = pa.latex_table(DATA, columns=["mass"], errors={"mass": "mass_err"},
                         decimals=1)
    assert r"$10.5 \pm 0.1$" in tex


def test_rounds_half_up_on_printed_digits():
    tex = pa.latex_table({"a": [2.675, 0.125]}, decimals=2)
    assert body(tex) == [r"2.68 \\", r"0.13 \\"]


def test_scientific_notation():
    tex = pa.latex_table({"f": [1.2345e-15, -5.6e-17, 5.0]},
                         notation="sci")
    assert body(tex) == [r"$1.23\times10^{-15}$ \\",
                         r"$-5.60\times10^{-17}$ \\", r"5.00 \\"]
    tex = pa.latex_table({"x": [1.234e-3], "e": [5.6e-5]},
                         errors={"x": "e"}, notation="sci")
    assert r"$(1.234 \pm 0.056)\times10^{-3}$" in tex
    tex = pa.latex_table({"x": [5.2e-3], "lo": [3e-4], "hi": [4e-4]},
                         errors={"x": ("lo", "hi")}, notation="sci",
                         decimals=1)
    assert r"$5.2^{+0.4}_{-0.3}\times10^{-3}$" in tex


def test_auto_notation_is_per_column():
    tex = pa.latex_table({"z": [0.0005, 2.0], "m": [1.2e10, 3.0e11],
                          "f": [2e-4, 5e-4]})
    assert body(tex)[0] == (r"0.000500 & $1.20\times10^{10}$ & "
                            r"$2.00\times10^{-4}$ \\")
    tex = pa.latex_table({"m": [1.2e10]}, notation={"m": "fixed"})
    assert body(tex) == [r"12000000000 \\"]


def test_integers_exact_unless_asked():
    tex = pa.latex_table({"id": [1073741824, -5], "x": [1.0, 2.0]}, sig=2)
    assert body(tex) == [r"1073741824 & 1.0 \\", r"$-5$ & 2.0 \\"]
    tex = pa.latex_table({"n": [1073741824]}, notation={"n": "sci"})
    assert r"$1.07\times10^{9}$" in tex


def test_missing_values():
    tex = pa.latex_table({"a": [1.0, None, np.nan], "s": ["x", None, "z"]},
                         missing="$\\cdots$")
    assert body(tex) == [r"1.00 & x \\", r"$\cdots$ & $\cdots$ \\",
                         r"$\cdots$ & z \\"]


def test_text_escaping_keeps_maths():
    tex = pa.latex_table({"name": ["A&B_1", "$w_0w_a$CDM", r"100\%"],
                          "col_1": [1, 2, 3]})
    rows = body(tex)
    assert rows[0].startswith(r"A\&B\_1")
    assert rows[1].startswith(r"$w_0w_a$CDM")
    assert rows[2].startswith(r"100\%")
    assert r"col\_1" in tex


def test_headers_units_and_align():
    tex = pa.latex_table(DATA, columns=["name", "mass"],
                         headers=["Galaxy", r"$\log M_\star$"],
                         units={"mass": r"$\mathrm{M_\odot}$"})
    assert r"\begin{tabular}{lc}" in tex
    assert r"Galaxy & $\log M_\star$ \\ & $\mathrm{M_\odot}$ \\" in flat(tex)
    tex = pa.latex_table(DATA, columns=["name", "mass"], align="l|r")
    assert r"\begin{tabular}{l|r}" in tex


def test_booktabs_bare_tabular_and_star():
    tex = pa.latex_table({"a": [1.0]}, booktabs=True, env=None)
    lines = [line.strip() for line in tex.splitlines()]
    assert lines[0] == r"% needs \usepackage{booktabs}"
    assert lines[1] == r"\begin{tabular}{c}"
    assert {r"\toprule", r"\midrule", r"\bottomrule"} <= set(lines)
    assert r"\begin{table" not in tex
    tex = pa.latex_table({"a": [1.0]}, env="table*")
    assert tex.startswith(r"\begin{table*}")
    assert tex.endswith(r"\end{table*}")


def test_numpy_inputs():
    arr = np.array([[1.0, 0.1, 2.5], [2.0, 0.25, 3.75]])
    tex = pa.latex_table(arr, errors={0: 1}, headers=["$a$", "$b$"], sig=1)
    assert body(tex) == [r"$1.0 \pm 0.1$ & 3 \\", r"$2.0 \pm 0.3$ & 4 \\"]

    rec = np.array([("a", 1.5), ("b", 2.5)],
                   dtype=[("name", "U1"), ("x", "f8")])
    tex = pa.latex_table(rec)
    assert r"name & x \\" in flat(tex)
    assert body(tex) == [r"a & 1.50 \\", r"b & 2.50 \\"]

    tex = pa.latex_table([["a", 1.5], ["b", 2]])        # list of rows
    assert body(tex) == [r"a & 1.50 \\", r"b & 2 \\"]


def test_pandas_dataframe():
    pd = pytest.importorskip("pandas")
    df = pd.DataFrame({"z": [0.1, 0.2], "z_err": [0.01, 0.02],
                       "n": pd.array([3, None], dtype="Int64")},
                      index=["x", "y"])
    tex = pa.latex_table(df, errors={"z": "z_err"})
    assert body(tex) == [r"$0.100 \pm 0.010$ & 3 \\",
                         r"$0.200 \pm 0.020$ & -- \\"]


def test_astropy_table_units_and_mask():
    table = pytest.importorskip("astropy.table")
    u = pytest.importorskip("astropy.units")
    t = table.QTable({"v": [123.456, 7.1] * u.km / u.s,
                      "v_err": [1.5, 0.25] * u.km / u.s,
                      "q": [0.5, 0.25]})
    tex = pa.latex_table(t, errors={"v": "v_err"})
    assert r"v & q \\ $\mathrm{km\,s^{-1}}$ & \\" in flat(tex)  # no unit: q
    assert body(tex) == [r"$123.5 \pm 1.5$ & 0.500 \\",
                         r"$7.10 \pm 0.25$ & 0.250 \\"]
    tex = pa.latex_table(t, errors={"v": "v_err"}, units={"v": "km/s"})
    assert r"v & q \\ km/s & \\" in flat(tex)
    assert "mathrm" not in pa.latex_table(t, units=False)

    m = table.Table({"a": table.MaskedColumn([1.0, 2.0], mask=[False, True])})
    assert body(pa.latex_table(m)) == [r"1.00 \\", r"-- \\"]


@pytest.mark.parametrize("kwargs, match", [
    ({"columns": ["nope"]}, "no column 'nope'"),
    ({"columns": ["z", "z_lo"], "errors": {"z": ("z_lo", "z_hi")}},
     "used as an error column"),
    ({"errors": {"z": "nope"}}, "no column 'nope'"),
    ({"errors": {"z": ("a", "b", "c")}}, "lower, upper"),
    ({"columns": ["mass"], "errors": {"z": "z_lo"}}, "not among the shown"),
    ({"sig": 2, "decimals": 1}, "not both"),
    ({"sig": {"z": 2}, "decimals": {"z": 1}}, "both sig and decimals"),
    ({"sig": 0}, "positive integer"),
    ({"decimals": -1}, "non-negative integer"),
    ({"notation": "eng"}, "notation must be"),
    ({"sig": {"zz": 2}}, "not among the table's columns"),
    ({"headers": ["one"]}, "got 1 entries"),
    ({"env": None, "caption": "x"}, "need an env"),
])
def test_bad_arguments(kwargs, match):
    with pytest.raises(ValueError, match=match):
        pa.latex_table(DATA, **kwargs)


def test_headers_must_be_list_or_dict():
    with pytest.raises(TypeError, match="list or a dict"):
        pa.latex_table(DATA, headers="name")


def test_unequal_columns():
    with pytest.raises(ValueError, match="same length"):
        pa.latex_table({"a": [1, 2], "b": [1]})
