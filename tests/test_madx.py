import pytest
import apace as ap

from scripts import test_output_dir, info, lattices_dir
from scripts.data_madx import twiss_plot, twiss_simulation


@pytest.fixture(scope="session")
def twiss_data():
    # TODO: make info addressable by name
    # name = "kuske_5bend_20p_reference.madx"
    lattice = info["lattices"][0]
    lattice_path = (lattices_dir / lattice["name"]).with_suffix(".madx")
    return twiss_simulation(lattice_path, lattice["energy"])


def test_twiss_plot(twiss_data):
    fig = twiss_plot(twiss_data)
    fig.savefig(test_output_dir / "twiss_madx.svg")