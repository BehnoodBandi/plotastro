# Installation

## From PyPI

```bash
pip install plotastro
```

To try the latest **beta** (a pre-release; plain `pip install` keeps giving
you the stable version):

```bash
pip install --pre plotastro                # or: pip install "plotastro==1.1.0b2"
pip install --pre "plotastro[cmasher]"     # the beta with CMasher
```

The only hard dependency is matplotlib (≥ 3.5). plotastro works with both
NumPy 1.x and 2.x — CI tests each — and with Python 3.9+. No LaTeX
installation is required (LaTeX text rendering is optional, see
{doc}`quickstart`).

### Optional: CMasher colours and colormaps

To use colours and colormaps from [CMasher](https://cmasher.readthedocs.io)
(see {doc}`colors`), install it as well:

```bash
pip install "plotastro[cmasher]"     # or simply: pip install cmasher
```

plotastro imports CMasher only when you ask for a CMasher colour, so it is
never needed otherwise. (Installing with conda? `conda install -c conda-forge cmasher`.)

## From a clone

```bash
git clone https://github.com/BehnoodBandi/plotastro
cd plotastro
pip install -e ".[dev]"          # editable install + test dependencies (incl. CMasher)
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
