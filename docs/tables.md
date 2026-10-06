# LaTeX tables

{func}`plotastro.latex_table` turns a pandas DataFrame, an astropy Table,
a NumPy array (structured or plain 2D) or a dict of columns into a LaTeX
table. You set the precision and notation of each column, and error
columns are merged into the column they belong to as `value ± error`
rather than being printed as columns of their own.

```python
import pandas as pd
import plotastro as pa

df = pd.DataFrame({
    "name":     ["NGC 1300", "NGC 4321", "M31"],
    "z":        [0.00526, 0.00524, -0.00100],
    "z_lo":     [0.00003, 0.00002, 0.00001],
    "z_hi":     [0.00004, 0.00002, 0.00001],
    "logM":     [10.523, 10.87, 11.04],
    "logM_err": [0.123, 0.05, 0.081],
    "flux":     [1.2345e-15, 3.4e-16, 5.61e-14],
})

print(pa.latex_table(
    df,
    errors={"z": ("z_lo", "z_hi"), "logM": "logM_err"},
    sig={"flux": 2},
    headers={"name": "Galaxy", "z": "$z$",
             "logM": r"$\log(M_\star/\mathrm{M_\odot})$", "flux": "$F$"},
    units={"flux": r"erg\,s$^{-1}$\,cm$^{-2}$"},
    caption="The galaxy sample.", label="tab:sample"))
```

```latex
\begin{table}
    \centering
    \caption{The galaxy sample.}
    \label{tab:sample}
    \begin{tabular}{lccc}
        \hline
        Galaxy   & $z$                                & $\log(M_\star/\mathrm{M_\odot})$ & $F$ \\
                 &                                    &                                  & erg\,s$^{-1}$\,cm$^{-2}$ \\
        \hline
        NGC 1300 & $0.005260^{+0.000040}_{-0.000030}$ & $10.52 \pm 0.12$                 & $1.2\times10^{-15}$ \\
        NGC 4321 & $0.005240 \pm 0.000020$            & $10.870 \pm 0.050$               & $3.4\times10^{-16}$ \\
        M31      & $-0.001000 \pm 0.000010$           & $11.040 \pm 0.081$               & $5.6\times10^{-14}$ \\
        \hline
    \end{tabular}
\end{table}
```

The layout follows the MNRAS template (caption above the table, `\hline`
rules), and the output compiles unchanged with all the journal classes
plotastro supports. The cells are padded so that the `&` separators line
up, which makes the source easy to edit by hand.

## Errors

`errors` maps each column to its error column(s):

| `errors=` | cell |
|---|---|
| `{"m": "m_err"}` | `$10.52 \pm 0.12$` |
| `{"z": ("z_lo", "z_hi")}` — (lower, upper) | `$1.235^{+0.034}_{-0.012}$` |

- Error columns are not printed on their own.
- Lower errors may be stored as negative numbers; only the magnitude is used.
- If the two asymmetric errors are equal after rounding, the cell shows
  `±` instead.
- If a row's error is missing, NaN or zero, that row shows the value on its
  own, formatted as a plain number.

## Precision and notation

Each option takes a single value for all columns, a `{column: value}` dict,
or a list with one entry per column shown.

`sig`
: Significant figures. The default is 3. For a column with errors, `sig`
  sets the significant figures of the **error** (default 2; for asymmetric
  errors, of the smaller one), and the value is rounded to the same decimal
  place: `1.23456 ± 0.0123` becomes `1.235 ± 0.012`. This is the usual
  convention for quoting measurements.

`decimals`
: A fixed number of digits after the decimal point, used instead of `sig`.
  In scientific notation it counts the digits of the mantissa. A column
  with errors shows the value and the error to the same number of decimals.

`notation`
: `"fixed"` gives `0.00123` and `"sci"` gives `$1.23\times10^{-3}$`.
  `"auto"` (the default) chooses once per column, so a column never mixes
  the two: it uses scientific notation when the column's largest absolute
  value is at least 10⁵ or below 10⁻³. With errors, the value and its error
  share one exponent: `$(1.234 \pm 0.056)\times10^{-3}$`.

Rounding is half-up on the decimal digits as you see them: `2.675` with
`decimals=2` gives `2.68`. Python's own `round` would give `2.67`, because
of how the number is stored in binary.

Integer columns, such as IDs and counts, are printed exactly. A plain
`sig=3` does not round them. They are formatted as numbers only if they
have errors or get their own entry, e.g. `notation={"N": "sci"}`.

## Headers, units and layout

- **Headers**: by default each header is the column name, with special
  characters escaped. Pass `headers` (a list, or a dict for only some
  columns) to use your own LaTeX, e.g. `r"$\log M_\star$"`.
- **Units**: `units` adds a second header row. The units of astropy
  columns are filled in automatically as LaTeX, e.g.
  `$\mathrm{km\,s^{-1}}$`. Entries in `units` replace them, and
  `units=False` removes the row.
- **Alignment**: by default text columns are `l` and numeric columns are
  `c`. `align="lrr"` sets your own spec; any `tabular` spec works,
  including `|` and `@{}`.
- **Environment**: `env="table*"` spans both columns of a two-column
  journal; `env=None` gives only the `tabular`.
- **booktabs**: `booktabs=True` uses `\toprule`/`\midrule`/`\bottomrule`.
  Your preamble then needs `\usepackage{booktabs}`.
- **Missing values**: `None`, NaN, masked astropy entries and `pandas.NA`
  are shown as `--` by default. Change this with e.g.
  `missing=r"$\cdots$"`.
- **Text cells** have `& % # _` escaped, except inside `$...$`, so maths
  like `$w_0w_a$CDM` works. LaTeX that is already escaped is left alone.

## Input types

| input | columns are referred to by |
|---|---|
| pandas DataFrame | column name (the index is not shown; use `df.reset_index()` to include it) |
| astropy `Table` / `QTable` | column name (units, masks and `Quantity` columns are supported) |
| NumPy structured array, dict of columns | field / key name |
| plain 2D array or list of rows | column index `0, 1, ...`, e.g. `errors={0: 1}`; set `headers=[...]` |

pandas and astropy are not plotastro dependencies. plotastro never imports
them: it reads any object that behaves like a DataFrame or a Table.
