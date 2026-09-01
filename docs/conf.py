"""Sphinx configuration for plotastro's documentation (Read the Docs)."""

import json
import re
import shutil
from importlib.metadata import PackageNotFoundError, version as get_version
from pathlib import Path

project = "plotastro"
author = "Behnood Bandi"
copyright = "2026, Behnood Bandi"

try:
    release = get_version("plotastro")
except PackageNotFoundError:
    release = "1.0.0"
version = ".".join(release.split(".")[:2])

extensions = [
    "myst_nb",                # markdown pages + rendered notebooks
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",    # numpy-style docstrings
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
]

myst_enable_extensions = ["colon_fence", "deflist"]
myst_heading_anchors = 3

# The tutorial notebook is committed already-executed; never re-run it here.
nb_execution_mode = "off"

exclude_patterns = ["_build", "jupyter_execute", "Thumbs.db", ".DS_Store"]

# Pull the notebook and the reference figures into the docs source tree so
# the build is self-contained (works identically locally and on RTD).
_docs = Path(__file__).resolve().parent
_repo = _docs.parent
shutil.copytree(_repo / "examples" / "figures", _docs / "_figures",
                dirs_exist_ok=True)

# The notebook's hand-written table of contents uses Jupyter-style anchors
# that don't exist in Sphinx (and Furo shows its own sidebar TOC), so strip
# those lines from the copy rendered here.
_nb = json.loads((_repo / "examples" / "tutorial.ipynb").read_text())
for _cell in _nb["cells"]:
    if _cell["cell_type"] == "markdown":
        _src = _cell["source"]
        _lines = _src.splitlines(True) if isinstance(_src, str) else _src
        _cell["source"] = [l for l in _lines
                           if not re.match(r"^\d+\.\s+\[.+\]\(#.+\)\s*$", l)]
(_docs / "tutorial.ipynb").write_text(json.dumps(_nb))

autodoc_member_order = "bysource"
autodoc_typehints = "none"
napoleon_google_docstring = False
napoleon_numpy_docstring = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
    "numpy": ("https://numpy.org/doc/stable", None),
}

html_theme = "furo"
html_title = f"plotastro {release}"
html_theme_options = {
    "source_repository": "https://github.com/BehnoodBandi/plotastro",
    "source_branch": "master",
    "source_directory": "docs/",
}
