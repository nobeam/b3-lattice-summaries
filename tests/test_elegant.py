from scripts import test_output_dir
from scripts.data_elegant import (
    twiss_plot,
    chroma_plot,
    simulation_elegant_dir,
    twiss_tables,
)

import pytest


@pytest.fixture(scope="session")
def twiss_data():
    from eleganttools import SDDS

    namespace = "kuske"
    name = "bessy3_5ba-20p_v_reference"
    return SDDS((simulation_elegant_dir / name).with_suffix(".twi")).as_dict()


def test_tables(twiss_data):
    import json

    path = test_output_dir / "elegant_twiss_tables.json"
    with path.open("w") as file:
        json.dump(twiss_tables(twiss_data), file)


def test_twiss_plot(twiss_data):
    fig = twiss_plot(twiss_data)
    fig.savefig(test_output_dir / "twiss_elegant.svg")


def test_chroma_plot(twiss_data):
    fig = chroma_plot(twiss_data)
    fig.savefig(test_output_dir / "chroma_elegant.svg")
