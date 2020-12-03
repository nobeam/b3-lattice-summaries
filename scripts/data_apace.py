import json

import apace as ap
import numpy as np
from matplotlib import rcParams

rcParams["font.family"] = "sans-serif"
rcParams["font.sans-serif"] = ["Inter"]
import matplotlib.pyplot as plt

from . import info, summary_dir, lattices_dir


def main():
    lattices = info["lattices"]
    n_lattices = len(lattices)

    print(f"\033[1;36m[Generating apace data 📈]\033[0m")
    for i, lattice in enumerate(lattices):
        name = lattice["name"]
        if "json" not in lattice["formats"]:
            print(f"\033[1m[{i+1}/{n_lattices}] Skipping {name} (no json file)\033[0m")
            continue

        output_dir = summary_dir / name / "apace"
        output_dir.mkdir(exist_ok=True, parents=True)

        print(f"\033[1m[{i+1}/{n_lattices}] Building {name}\033[0m")
        lattice_obj = ap.Lattice.from_file((lattices_dir / name).with_suffix(".json"))
        twiss_data = ap.Twiss(
            lattice_obj, energy=lattice["energy"], steps_per_meter=100
        )

        print(f"    Generating tables 📝")
        with (output_dir / "twiss_tables.json").open("w") as file:
            json.dump(twiss_tables(twiss_data), file)

        print(f"    Generating twiss plot 📊")
        twiss_plot(twiss_data).savefig(output_dir / "twiss.svg")


def twiss_tables(twiss: ap.Twiss):
    """Returns the relevant elgant data as dict"""
    return {
        "machine_parameters": [
            ["Energy", twiss.energy],
            ["Cell length", twiss.lattice.length],
            ["Mom. compaction", twiss.alpha_c],
        ],
        "twiss_x": [
            ["Tune x", twiss.tune_x],
            # ["Chromaticity x", twiss.chromaticity_x], # TODO: fix chroma in apace
            ["max beta x", np.max(twiss.beta_x)],
            ["min beta x", np.min(twiss.beta_x)],
            ["mean beta x", np.mean(twiss.beta_x)],
            ["max eta x", np.max(twiss.eta_x)],
        ],
        "twiss_y": [
            ["Tune y", twiss.tune_y],
            # ["Chromaticity y", twiss.chromaticity_y], # TODO: fix chroma in apace
            ["max beta y", np.max(twiss.beta_y)],
            ["min beta y", np.min(twiss.beta_y)],
            ["mean beta y", np.mean(twiss.beta_y)],
            ["max eta y", 0],
        ],
        "synchrotron_radiation_integrals": [
            ["I1", twiss.i1],
            ["I2", twiss.i2],
            ["I3", twiss.i3],
            ["I4", twiss.i4],
            ["I5", twiss.i5],
            ["Emittance", twiss.emittance_x],
        ],
    }


def twiss_plot(twiss: ap.Twiss):
    import apace.plot as aplot
    from math import log10, floor

    fig, ax = plt.subplots(figsize=(8, 5))
    factor = np.max(twiss.beta_x) / np.max(twiss.eta_x)
    eta_x_scale = 10 ** floor(log10(factor))
    aplot.plot_twiss(ax, twiss, scales={"eta_x": eta_x_scale})
    aplot.draw_lattice(ax, twiss.lattice, labels=twiss.lattice.length < 30)
    fig.tight_layout()
    return fig
