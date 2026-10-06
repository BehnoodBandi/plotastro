"""LaTeX tables from NumPy arrays, pandas DataFrames and astropy Tables.

    import plotastro as pa
    print(pa.latex_table(df, errors={"mass": "mass_err"}, sig={"z": 4},
                         caption="The galaxy sample.", label="tab:sample"))

Each column is formatted on its own: a number of significant figures
(``sig``) or of decimal places (``decimals``), in fixed-point or scientific
``notation``. Columns named in ``errors`` are folded into the column they
belong to, as ``$1.23 \\pm 0.05$`` (or ``$1.23^{+0.06}_{-0.04}$`` for
asymmetric errors), instead of getting a column of their own.

The layout follows the MNRAS template (caption above, ``\\hline`` rules),
which compiles unchanged with every journal class plotastro knows.
"""

from __future__ import annotations

import math
import numbers
import re
from collections.abc import Mapping
from decimal import ROUND_HALF_UP, Context, Decimal

import numpy as np

_NOTATIONS = {"auto": "auto", "fixed": "fixed", "sci": "sci",
              "scientific": "sci"}
_SIG = 3        # default significant figures of a plain number
_SIG_ERR = 2    # ... and of an uncertainty
# notation="auto" makes a column scientific when its largest |value| is
# outside [_AUTO_LOW, _AUTO_HIGH)
_AUTO_LOW, _AUTO_HIGH = 1e-3, 1e5

# enough digits to print any float without an exponent
_CONTEXT = Context(prec=1000)

_SPECIAL = re.compile(r"(?<!\\)([&%#_])")


def _escape_text(text):
    """Escape unescaped & % # _ outside $...$; leave existing LaTeX alone."""
    if isinstance(text, bytes):
        text = text.decode()
    segments = re.split(r"(?<!\\)\$", str(text).strip())
    return "$".join(_SPECIAL.sub(r"\\\1", seg) if i % 2 == 0 else seg
                    for i, seg in enumerate(segments))


def _read_columns(data):
    """({name: list of cells}, {name: unit}) for any supported input."""
    if hasattr(data, "colnames"):                          # astropy Table
        cols = {name: list(getattr(data[name], "value", data[name]))
                for name in data.colnames}
        units = {name: getattr(data[name], "unit", None)
                 for name in data.colnames}
    elif hasattr(data, "columns") and hasattr(data, "iloc"):   # DataFrame
        cols, units = {name: list(data[name]) for name in data.columns}, {}
    elif isinstance(data, Mapping):                        # {name: column}
        cols, units = {name: list(col) for name, col in data.items()}, {}
    else:
        arr = (data if isinstance(data, np.ndarray)
               else np.asarray(data, dtype=object))
        if arr.dtype.names:                                # structured array
            cols = {name: list(arr[name]) for name in arr.dtype.names}
        else:                                              # 1D or 2D array
            if arr.ndim == 1:
                arr = arr[:, None]
            if arr.ndim != 2:
                raise ValueError(
                    f"Expected a 1D or 2D array, got {arr.ndim} dimensions.")
            cols = {j: list(arr[:, j]) for j in range(arr.shape[1])}
        units = {}
    if len({len(col) for col in cols.values()}) > 1:
        raise ValueError("All columns must have the same length.")
    return cols, units


def _is_missing(x):
    if x is None or x is np.ma.masked:
        return True
    try:
        return bool(x != x)          # NaN
    except TypeError:                # pandas.NA refuses to be a bool
        return True


def _is_number(x):
    return (isinstance(x, numbers.Real)
            and not isinstance(x, (bool, np.bool_)))


def _round(x, place):
    """x rounded half-up at 10**place, as a Decimal.

    Rounds the decimal digits Python prints for x (2.675 -> 2.68, 0.25 ->
    0.3), not its binary value, so ties go the way a reader expects.
    """
    return Decimal(repr(float(x))).quantize(
        Decimal(1).scaleb(place), rounding=ROUND_HALF_UP, context=_CONTEXT)


def _sig_place(x, sig):
    """Power of ten of the last of `sig` significant figures of x
    (0.01234, 2 -> -3; 1234, 2 -> 2; 9.96, 2 -> 0 as it rounds to 10)."""
    d = Decimal(repr(float(x)))
    if not d:
        return 1 - sig
    place = d.adjusted() + 1 - sig
    if _round(x, place).adjusted() > d.adjusted():
        place += 1
    return place


def _number(value, errs, sig_value, sig_error, decimals, sci):
    """LaTeX for a value with (), (err,) or (lower, upper) uncertainties."""
    value = float(value)
    if math.isinf(value):
        return r"$\infty$" if value > 0 else r"$-\infty$"
    errs = [abs(float(e)) for e in errs]
    if not all(math.isfinite(e) and e > 0 for e in errs):
        errs = []                    # missing/zero error: plain value

    # `place`: power of ten of the last digit shown
    if decimals is not None:
        place = _sig_place(value, decimals + 1) if sci else -decimals
    elif errs:                       # the uncertainty sets the precision
        place = _sig_place(min(errs), sig_error)
    else:
        place = _sig_place(value, sig_value)

    exp = 0
    if sci:                          # exponent of the value, as rounded
        ref = _round(value, place)
        if not ref and errs:
            ref = _round(max(errs), place)
        exp = ref.adjusted() if ref else 0

    def show(x):
        rounded = _round(x, place)
        text = f"{rounded.scaleb(-exp, _CONTEXT):f}"
        return text.lstrip("-") if not rounded else text   # no "-0.00"

    body = show(value)
    if errs:
        if len(errs) == 1 or show(errs[0]) == show(errs[1]):
            body = f"{body} \\pm {show(errs[-1])}"
            if exp:
                body = f"({body})"
        else:
            lower, upper = errs
            body = f"{body}^{{+{show(upper)}}}_{{-{show(lower)}}}"
    if exp:
        body += f"\\times10^{{{exp}}}"
    return f"${body}$" if any(c in body for c in "-\\^") else body


def _per_column(option, keys, what):
    """Split an option into ({column: value}, value for all other columns).

    It can be one value for every column, a {column: value} mapping, or a
    list with one value per shown column.
    """
    if isinstance(option, Mapping):
        unknown = [k for k in option if k not in keys]
        if unknown:
            raise ValueError(
                f"{what}: {unknown} not among the table's columns "
                f"{list(keys)}.")
        return dict(option), None
    if isinstance(option, (list, tuple)):
        if len(option) != len(keys):
            raise ValueError(
                f"{what}: got {len(option)} entries for {len(keys)} columns.")
        return dict(zip(keys, option)), None
    return {}, option


def _resolve_errors(errors, cols):
    """{column: tuple of its error columns}, checked against the data."""
    resolved = {}
    for name, err in (errors or {}).items():
        err = tuple(err) if isinstance(err, (list, tuple)) else (err,)
        if len(err) not in (1, 2):
            raise ValueError(
                f"errors[{name!r}] must be one column (symmetric) or a "
                f"(lower, upper) pair, got {err!r}.")
        for key in (name,) + err:
            if key not in cols:
                raise ValueError(
                    f"errors: no column {key!r} in the data "
                    f"(columns: {list(cols)}).")
        resolved[name] = err
    return resolved


def latex_table(data, columns=None, *, errors=None, sig=None, decimals=None,
                notation="auto", headers=None, units=None, align=None,
                caption=None, label=None, env="table", booktabs=False,
                missing="--"):
    r"""LaTeX table from a NumPy array, pandas DataFrame or astropy Table.

    Parameters
    ----------
    data : DataFrame, astropy Table, structured or 2D array, or dict
        The table. Columns are referred to by name; the columns of a plain
        2D array (or list of rows) by their index ``0, 1, ...``. A
        DataFrame's index is not shown (use ``df.reset_index()`` for that).
    columns : list, optional
        Columns to show, in order. Default: all of them except those used
        as errors.
    errors : dict, optional
        ``{column: error_column}`` puts ``value \pm error`` in that column;
        ``{column: (lower, upper)}`` gives ``value^{+upper}_{-lower}``
        (signs of the errors are ignored). Error columns are not shown on
        their own. A missing, zero or NaN error leaves the value alone.
    sig : int or dict, optional
        Significant figures. For a column with errors this is the number
        of significant figures of the (smaller) error, and the value is
        rounded to the same decimal place — the usual convention for
        quoting measurements. Default: 3, or 2 for errors.
    decimals : int or dict, optional
        Digits after the decimal point (of the mantissa, in scientific
        notation), instead of ``sig``; for a column with errors the value
        and the error get the same number.
    notation : {"auto", "fixed", "sci"} or dict
        ``"fixed"`` gives ``0.00123``, ``"sci"`` gives
        ``1.23\times10^{-3}``. ``"auto"`` (default) chooses per column:
        scientific when the largest absolute value is at least 1e5 or
        below 1e-3.
    headers : list or dict, optional
        Header row: a list with one entry per shown column, or
        ``{column: header}``. Headers are used as LaTeX as given, so maths
        like ``r"$\log M_\star$"`` works. Default: the column names,
        escaped.
    units : list or dict or False, optional
        A second header row of units, given as LaTeX. Units of astropy
        columns are filled in automatically (entries given here replace
        them); ``units=False`` leaves the row out.
    align : str, optional
        The ``tabular`` column specification, e.g. ``"lcc"`` or ``"l|rr"``.
        Default: ``l`` for text columns, ``c`` for numeric ones.
    caption, label : str, optional
        ``\caption`` (LaTeX, used as given) and ``\label`` of the table.
    env : str or None
        Environment wrapped around the ``tabular``: ``"table"`` (default),
        ``"table*"`` for a table spanning both columns of a two-column
        journal, or ``None`` for the bare ``tabular``.
    booktabs : bool
        Use ``\toprule``/``\midrule``/``\bottomrule`` (needs
        ``\usepackage{booktabs}``) instead of ``\hline``.
    missing : str
        Shown for missing values: None, NaN, masked entries, pandas.NA.

    Integer columns are shown exactly, unless they have errors or their own
    entry in ``sig``, ``decimals`` or ``notation``. Text is escaped
    (``& % # _`` outside ``$...$``); LaTeX already in it is left alone.

    Returns
    -------
    str : LaTeX source to paste into your manuscript.

    Examples
    --------
    >>> print(pa.latex_table(df, errors={"mass": "mass_err",
    ...                                  "z": ("z_lo", "z_hi")},
    ...                      sig={"z": 2}, notation={"flux": "sci"},
    ...                      headers={"mass": r"$\log M_\star$"},
    ...                      caption="The sample.", label="tab:sample"))
    """
    cols, data_units = _read_columns(data)
    errs = _resolve_errors(errors, cols)
    error_cols = {e for err in errs.values() for e in err}

    if columns is None:
        columns = [c for c in cols if c not in error_cols]
    else:
        columns = list(columns)
        for c in columns:
            if c not in cols:
                raise ValueError(
                    f"columns: no column {c!r} in the data "
                    f"(columns: {list(cols)}).")
            if c in error_cols:
                raise ValueError(
                    f"columns: {c!r} is used as an error column, so it is "
                    f"shown with the column it belongs to.")
    for name in errs:
        if name not in columns:
            raise ValueError(
                f"errors: column {name!r} is not among the shown columns.")
    if not columns:
        raise ValueError("No columns to show.")

    sig_col, sig_all = _per_column(sig, columns, "sig")
    dec_col, dec_all = _per_column(decimals, columns, "decimals")
    nota_col, nota_all = _per_column(notation, columns, "notation")
    if sig_all is not None and dec_all is not None:
        raise ValueError("Give sig or decimals, not both.")

    body_cols = []
    for c in columns:
        s, d = sig_col.get(c), dec_col.get(c)
        if s is not None and d is not None:
            raise ValueError(
                f"Column {c!r} has both sig and decimals; give one.")
        if s is None and d is None:
            s, d = sig_all, dec_all
        if s is not None and (not isinstance(s, numbers.Integral) or s < 1):
            raise ValueError(f"sig must be a positive integer, got {s!r}.")
        if d is not None and (not isinstance(d, numbers.Integral) or d < 0):
            raise ValueError(
                f"decimals must be a non-negative integer, got {d!r}.")
        nota = nota_col.get(c, nota_all if nota_all is not None else "auto")
        if nota not in _NOTATIONS:
            raise ValueError(
                f"notation must be 'auto', 'fixed' or 'sci', got {nota!r}.")
        nota = _NOTATIONS[nota]

        cells = cols[c]
        err_cells = [cols[e] for e in errs.get(c, ())]
        # integers are exact unless the column is treated as measurements
        exact_ints = not (err_cells or c in sig_col or c in dec_col
                          or c in nota_col)
        if nota == "auto":
            sizes = [abs(float(x)) for x in cells if _is_number(x)
                     and not _is_missing(x) and math.isfinite(x)]
            biggest = max(sizes, default=0)
            nota = ("sci" if biggest >= _AUTO_HIGH
                    or 0 < biggest < _AUTO_LOW else "fixed")

        out = []
        for i, x in enumerate(cells):
            if _is_missing(x):
                out.append(missing)
            elif not _is_number(x):
                out.append(_escape_text(x))
            elif exact_ints and isinstance(x, numbers.Integral):
                out.append(f"${int(x)}$" if x < 0 else str(int(x)))
            else:
                e = tuple(ec[i] for ec in err_cells)
                if any(_is_missing(v) or not _is_number(v) for v in e):
                    e = ()
                out.append(_number(
                    x, e, sig_value=_SIG if err_cells else s or _SIG,
                    sig_error=s or _SIG_ERR, decimals=d,
                    sci=nota == "sci"))
        body_cols.append(out)

    # header and units rows
    for what, option in (("headers", headers), ("units", units)):
        if option not in (None, False) and not isinstance(
                option, (Mapping, list, tuple)):
            raise TypeError(f"{what} must be a list or a dict, "
                            f"got {type(option).__name__}.")
    head_col, _ = _per_column(headers or {}, columns, "headers")
    head = [str(head_col[c]) if c in head_col else _escape_text(c)
            for c in columns]
    unit_row = []
    if units is not False:
        unit_col, _ = _per_column(units or {}, columns, "units")
        for c in columns:
            u = unit_col.get(c, data_units.get(c))
            if u is not None and not isinstance(u, str):    # astropy unit
                u = u.to_string("latex_inline") if str(u) else ""
            unit_row.append(u or "")

    if align is None:
        align = "".join(
            "c" if any(_is_number(x) and not _is_missing(x)
                       for x in cols[c]) else "l" for c in columns)

    rows = [head] + ([unit_row] if any(unit_row) else [])
    n_head = len(rows)
    rows += [list(r) for r in zip(*body_cols)]
    widths = [max(len(r[j]) for r in rows) for j in range(len(columns))]
    lines = [" & ".join(cell.ljust(w) for cell, w in zip(r, widths)).rstrip()
             + r" \\" for r in rows]

    top, mid, bottom = ((r"\toprule", r"\midrule", r"\bottomrule")
                        if booktabs else (r"\hline",) * 3)
    tabular = ([f"\\begin{{tabular}}{{{align}}}", f"    {top}"]
               + [f"    {line}" for line in lines[:n_head]]
               + [f"    {mid}"]
               + [f"    {line}" for line in lines[n_head:]]
               + [f"    {bottom}", r"\end{tabular}"])

    if env is None:
        if caption is not None or label is not None:
            raise ValueError("caption and label need an env, e.g. "
                             "env='table'.")
        out = tabular
    else:
        out = [f"\\begin{{{env}}}", r"    \centering"]
        if caption is not None:
            out.append(f"    \\caption{{{caption}}}")
        if label is not None:
            out.append(f"    \\label{{{label}}}")
        out += [f"    {line}" for line in tabular] + [f"\\end{{{env}}}"]
    if booktabs:
        out.insert(0, r"% needs \usepackage{booktabs}")
    return "\n".join(out)
