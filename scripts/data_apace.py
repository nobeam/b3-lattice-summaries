import json

import apace as ap
import numpy as np
import matplotlib.pyplot as plt

from . import info, summary_dir, lattices_generated_dir


def main():
    lattices = info["lattices"]
    n_lattices = len(lattices)

    print(f"\033[1;36m[Generating apace data 📈]\033[0m")
    for i, lattice in enumerate(lattices):
        name = lattice["name"]
        if "json" not in lattice["formats"]:
            print(f"\033[1m[{i+1}/{n_lattices}] Skipping {name} (no json file)\033[0m")
            continue

        print(f"\033[1m[{i+1}/{n_lattices}] \033[0m", end="")
        data(lattice)


def data(lattice):
    name = lattice["name"]
    print(f"\033[1mGenerating data for {name}\033[0m")

    output_dir = summary_dir / name / "apace"
    output_dir.mkdir(exist_ok=True, parents=True)

    print(f"    Compute simulation data")
    lattice_obj = ap.Lattice.from_file(
        (lattices_generated_dir / name).with_suffix(".json")
    )
    twiss_data = ap.Twiss(lattice_obj, energy=lattice["energy"], steps_per_meter=100)

    print(f"    Generating tables 📝")
    with (output_dir / "twiss_tables.json").open("w") as file:
        json.dump(twiss_tables(twiss_data), file)

    print(f"    Generating twiss plot 📊")
    twiss_plot(twiss_data).savefig(output_dir / "twiss.svg")

    print(f"    Generating floor plan 📊")
    fig_ring, fig_cell = floor_plan_plot(lattice_obj)
    fig_ring.savefig(output_dir / "floor_plan_ring.svg")
    fig_cell.savefig(output_dir / "floor_plan_cell.svg")


def twiss_tables(twiss: ap.Twiss):
    """Returns the relevant elgant data as dict"""
    return [
        [
            "Global Machine & Lattice Parameter",
            [
                [
                    ["Energy", twiss.energy],
                    ["Cell length", twiss.lattice.length],
                    ["Mom. compaction", twiss.alpha_c],
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
                    ["Tune x", twiss.tune_x],
                    # TODO: fix chroma in apace
                    # ["Chromaticity x", twiss.chromaticity_x],
                    ["max beta x", np.max(twiss.beta_x)],
                    ["min beta x", np.min(twiss.beta_x)],
                    ["mean beta x", np.mean(twiss.beta_x)],
                    ["max eta x", np.max(twiss.eta_x)],
                ],
                [
                    ["Tune y", twiss.tune_y],
                    # TODO: fix chroma in apace
                    # ["Chromaticity y", twiss.chromaticity_y],
                    ["max beta y", np.max(twiss.beta_y)],
                    ["min beta y", np.min(twiss.beta_y)],
                    ["mean beta y", np.mean(twiss.beta_y)],
                    ["max eta y", 0],
                ],
            ],
        ],
        [
            "Synchrotron Radiation Integrals",
            [
                [
                    ["I1", twiss.i1],
                    ["I2", twiss.i2],
                    ["I3", twiss.i3],
                    ["I4", twiss.i4],
                    ["I5", twiss.i5],
                    ["Emittance", twiss.emittance_x],
                ]
            ],
        ],
        [
            "Floor plan",
            ["floor_plan_ring.svg", "floor_plan_cell.svg"],
        ],
    ]


def twiss_plot(twiss: ap.Twiss):
    from math import log10, floor
    from apace.plot import draw_elements, plot_twiss

    fig, ax = plt.subplots(figsize=(8, 5))
    factor = np.max(twiss.beta_x) / np.max(twiss.eta_x)
    eta_x_scale = 10 ** floor(log10(factor))
    plot_twiss(ax, twiss, scales={"eta_x": eta_x_scale})
    draw_elements(ax, twiss.lattice, labels=twiss.lattice.length < 30)
    fig.tight_layout()
    return fig


def floor_plan_plot(lattice: ap.Lattice):
    from apace.plot import floor_plan

    fig_ring, ax = plt.subplots()
    ax.axis("off")
    floor_plan(ax, lattice, labels=False)

    fig_cell, ax = plt.subplots()
    ax.axis("off")
    cell = lattice.tree[0]
    floor_plan(ax, cell)

    return fig_ring, fig_cell
