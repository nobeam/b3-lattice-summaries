from scripts import test_output_dir
from scripts.data_elegant import twiss_plot, chroma_plot, simulation_elegant_dir
from eleganttools import SDDS

import pytest


@pytest.fixture(scope="session")
def elegant_twiss_data():
    name = "5bend_20p_LongBend-TG-TGRB.twi"
    return SDDS((simulation_elegant_dir / name)).as_dict()


def test_twiss_plot(elegant_twiss_data):
    fig = twiss_plot(elegant_twiss_data)
    fig.savefig(test_output_dir / "twiss_elegant.svg")


def test_chroma_plot(elegant_twiss_data):
    fig = chroma_plot(elegant_twiss_data)
    fig.savefig(test_output_dir / "chroma_elegant.svg")
