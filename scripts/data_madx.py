import json

from cpymad.madx import Madx
import numpy as np
import matplotlib.pyplot as plt

from . import info, summary_dir, lattices_generated_dir


def main():
    lattices = info["lattices"]
    n_lattices = len(lattices)

    print(f"\033[1;36m[Generating madx data 📈]\033[0m")
    for i, lattice in enumerate(lattices):
        name = lattice["name"]
        if "madx" not in lattice["formats"]:
            print(f"\033[1m[{i+1}/{n_lattices}] Skipping {name} (no madx file)\033[0m")
            continue

        print(f"\033[1m[{i+1}/{n_lattices}] \033[0m", end="")
        data(lattice)


def data(lattice):
    name = lattice["name"]
    print(f"\033[1mGenerating data for {name}\033[0m")

    print(f"    Run madx simulation ⚙ {name}")
    lattice_path = (lattices_generated_dir / name).with_suffix(".madx")
    twiss_data = twiss_simulation(lattice_path, lattice["energy"])

    output_dir = summary_dir / name / "madx"
    output_dir.mkdir(exist_ok=True, parents=True)

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
    """Returns the relevant elgant data as dict"""
    twiss = twiss.summary
    return [
        [
            "Global Machine & Lattice Parameter",
            [
                [
                    ["Energy", twiss.energy],
                    ["Energy", twiss.energy],
                    ["Cell length", twiss.length],
                    ["Mom. compaction", twiss.alfa],
                ],
            ],
        ],
        [
            "Optical Functions",
            ["twiss.svg"],
        ],
        [
            "Detailed Lattice Parameter",
            [
                [
                    ["Tune x", twiss.q1],
                    ["Chromaticity x", twiss.dq1],
                    ["max beta x", twiss.betxmax],
                ],
                [
                    ["Tune y", twiss.q2],
                    ["Chromaticity y", twiss.dq2],
                    ["max beta y", twiss.betxmax],
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
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(twiss["s"], twiss["betx"], "#EF4444")
    ax.plot(twiss["s"], twiss["bety"], "#1D4ED8")
    ax.plot(twiss["s"], eta_x_scale * twiss["dx"], "#10B981")
    ax.grid(color="#E5E7EB", linestyle="--", linewidth=1)
    fig.tight_layout()
    return fig
