import pytest
import apace as ap

from scripts import test_output_dir, lattices_generated_dir
from scripts.data_apace import twiss_plot, floor_plan_plot


@pytest.fixture(scope="session")
def lattice():
    namespace = "kuske"
    name = "bessy3_5ba-20p_v_reference"
    path = (lattices_generated_dir / namespace / name).with_suffix(".json")
    return ap.Lattice.from_file(path)


@pytest.fixture(scope="session")
def twiss_data(lattice):
    return ap.Twiss(lattice, energy=2500)


def test_twiss_plot(twiss_data):
    fig = twiss_plot(twiss_data)
    fig.savefig(test_output_dir / "apace_twiss.svg")


def test_floor_plan_plot(lattice):
    fig_ring, fig_cell = floor_plan_plot(lattice)
    fig_ring.savefig(test_output_dir / "apace_floor_plan_ring.svg")
    fig_cell.savefig(test_output_dir / "apace_floor_plan_cell.svg")
