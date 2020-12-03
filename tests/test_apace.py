import pytest
import apace as ap

from scripts import test_output_dir, lattices_dir
from scripts.data_apace import twiss_plot


@pytest.fixture(scope="session")
def twiss_data():
    name = "kuske_5bend_20p_reference.json"
    lattice = ap.Lattice.from_file(lattices_dir / name)
    return ap.Twiss(lattice, energy=2500)


def test_twiss_plot(twiss_data):
    fig = twiss_plot(twiss_data)
    fig.savefig(test_output_dir / "twiss_apace.svg")