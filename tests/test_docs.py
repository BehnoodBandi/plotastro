"""The API reference (docs/api/) must document every public name, and the
constant values it shows must match the code."""

import ast
import re
import textwrap
from pathlib import Path

import pytest

import plotastro as pa

API_DIR = Path(__file__).resolve().parents[1] / "docs" / "api"

# Public names deliberately left out of the documentation.
UNDOCUMENTED = {"euclid_colors"}


def test_every_public_name_is_in_the_api_reference():
    text = "\n".join(page.read_text(encoding="utf-8")
                     for page in API_DIR.glob("*.md"))
    documented = set(re.findall(
        r"^\.\. (?:autofunction|py:function|py:data):: (?:plotastro\.)?(\w+)",
        text, re.MULTILINE))
    missing = sorted(set(pa.__all__) - documented - UNDOCUMENTED)
    assert not missing, f"public names missing from docs/api/: {missing}"


def documented_value(page, name):
    """The Python code block under ``.. py:data:: name`` on a page."""
    text = (API_DIR / page).read_text(encoding="utf-8")
    entry = text.split(f".. py:data:: {name}\n", 1)[1]
    block = entry.split(".. code-block:: python\n", 1)[1]
    lines = []
    for line in block.splitlines()[1:]:          # skip the blank line
        if line.strip() and not line.startswith("      "):
            break
        lines.append(line)
    return ast.literal_eval(textwrap.dedent("\n".join(lines)))


@pytest.mark.parametrize("page, name", [
    ("colors.md", "COLORS"), ("colors.md", "OKABE_ITO"),
    ("colors.md", "PETROFF8"), ("colors.md", "PETROFF10"),
    ("colors.md", "TOL_VIBRANT"), ("colors.md", "PAIRED"),
    ("markers.md", "MARKERS"), ("markers.md", "LINESTYLES"),
])
def test_documented_constants_match_the_code(page, name):
    assert documented_value(page, name) == getattr(pa, name)
