from pathlib import Path

from scripts import test_output_dir
from scripts.elegant import chroma_plot, simulation_elegant_dir
from eleganttools import SDDS


def test_chroma_plot():
    name = "5bend_20p_LongBend-TG-TGRB"
    data = SDDS((simulation_elegant_dir / name).with_suffix(".twi")).as_dict()
    chroma_plot(data).savefig((test_output_dir / name).with_suffix(".svg"))
