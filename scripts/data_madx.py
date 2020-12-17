import json
from operator import itemgetter

from cpymad.madx import Madx
import numpy as np
import matplotlib.pyplot as plt

from . import FIG_SIZE, lattices_generated_dir


def results(lattice, output_dir):
    output_dir.mkdir(exist_ok=True, parents=True)
    name, namespace = itemgetter("name", "namespace")(lattice)
    print(f"\033[1m[MAD-X] Generating results for {namespace}/{name}\033[0m")

    print(f"    Run madx simulation ⚙ {name}")
    lattice_path = (lattices_generated_dir / namespace / name).with_suffix(".madx")
    twiss_data = twiss_simulation(lattice_path, lattice["energy"])

    print(f"    Generating tables 📝")
    with (output_dir / "twiss_tables.json").open("w") as file:
        json.dump(twiss_tables(twiss_data), file)

    print(f"    Generating twiss plot 📊")
    twiss_plot(twiss_data).savefig(output_dir / "twiss.svg")


def twiss_simulation(path, energy):
    madx = Madx(stdout=False)
    madx.options.info = False
    madx.command.beam(particle="electron", energy=energy, charge=-1)
    madx.input(path.read_text())
    return madx.twiss(chrom=True)


def twiss_tables(twiss):
    twiss = twiss.summary
    return [
        [
            "Optical Functions",
            ["twiss.svg"],
        ],
        [
            "Detailed Lattice Parameter",
            [
                [
                    ["Energy", twiss.energy],
                    ["Mom. compaction", twiss.alfa],
                    ["transition energy", twiss.gammatr],
                ],
                [
                    ["tune x", twiss.q1],
                    ["chromaticity x", twiss.dq1],
                    ["max beta x", twiss.betxmax],
                    ["max eta x", twiss.dxmax],
                ],
                [
                    ["Tune y", twiss.q2],
                    ["Chromaticity y", twiss.dq2],
                    ["max beta y", twiss.betxmax],
                    ["max eta y", twiss.dymax],
                ],
            ],
        ],
        [
            "Synchrotron Radiation Integrals",
            [
                [
                    ["I1", twiss.synch_1],
                    ["I2", twiss.synch_2],
                    ["I3", twiss.synch_3],
                    ["I4", twiss.synch_4],
                    ["I5", twiss.synch_5],
                ]
            ],
        ],
    ]


def twiss_plot(twiss):
    from math import log10, floor

    factor = np.max(twiss.summary.betxmax) / np.max(twiss.summary.dxmax)
    eta_x_scale = 10 ** floor(log10(factor))
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    ax.plot(twiss["s"], twiss["betx"], "#EF4444")
    ax.plot(twiss["s"], twiss["bety"], "#1D4ED8")
    ax.plot(twiss["s"], eta_x_scale * twiss["dx"], "#10B981")
    ax.grid(color="#E5E7EB", linestyle="--", linewidth=1)
    ax.set_xlim(0, 20)  # TODO: use cell length!
    fig.tight_layout()
    return fig
