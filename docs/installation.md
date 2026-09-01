# Installation

## From PyPI

```bash
pip install plotastro
```

The only hard dependency is matplotlib (≥ 3.5). plotastro works with both
NumPy 1.x and 2.x — CI tests each — and with Python 3.9+. No LaTeX
installation is required (LaTeX text rendering is optional, see
{doc}`quickstart`).

## From a clone

```bash
git clone https://github.com/BehnoodBandi/plotastro
cd plotastro
pip install -e ".[dev]"          # editable install + test dependencies
pytest                           # optional: run the test suite
```

To run the examples and notebook from a clone:

```bash
pip install -r requirements-dev.txt
```

## Styles only, no package

If you just want the `.mplstyle` files, copy them from
`src/plotastro/styles/` into your matplotlib configuration directory:

```python
import matplotlib
print(matplotlib.get_configdir())   # copy the files into <this>/stylelib/
```

After that, `plt.style.use("mnras")` works in any script without plotastro
installed. (With the package installed, this step is unnecessary —
importing plotastro registers the styles automatically.)
