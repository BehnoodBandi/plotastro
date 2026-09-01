import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest


@pytest.fixture(autouse=True)
def _clean_state():
    yield
    plt.close("all")
    matplotlib.rcdefaults()
