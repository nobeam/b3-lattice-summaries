import json
from itertools import groupby
from operator import itemgetter

import apace as ap
import numpy as np
import matplotlib.pyplot as plt

from . import FIG_SIZE, lattices_generated_dir


def results(lattice, output_dir):
    output_dir.mkdir(exist_ok=True, parents=True)
    name, namespace = itemgetter("name", "namespace")(lattice)
    print(f"\033[1m[apace] Generating results for {namespace}/{name}\033[0m")

    print(f"    Compute simulation data")
    lattice_path = (lattices_generated_dir / namespace / name).with_suffix(".json")
    lattice_obj = ap.Lattice.from_file(lattice_path)
    twiss_data = ap.Twiss(lattice_obj, energy=lattice["energy"], steps_per_meter=100)

    print(f"    Generating tables 📝")
    with (output_dir / "twiss_tables.json").open("w") as file:
        json.dump(twiss_tables(twiss_data), file)

    print(f"    Generating twiss plot 📊")
    twiss_plot(twiss_data).savefig(output_dir / "twiss.svg")

    print(f"    Generating floor plan 📊")
    floor_plan_plot(lattice_obj).savefig(output_dir / "floor_plan_cell.svg")


def twiss_tables(twiss: ap.Twiss):
    """Returns the relevant elgant data as dict"""
    lattice = twiss.lattice
    cell = twiss.lattice.children[0]
    # do not count consecutive dipoles
    bends = [
        element
        for element, _ in groupby(cell.sequence)
        if isinstance(element, ap.Dipole)
    ]
    n_bends = sum(bend.angle > 0 for bend in bends)
    n_reverse_bends = len(bends) - n_bends
    return [
        [
            "Global Machine & Lattice Parameter",
            [
                [
                    ["Energy", twiss.energy],
                    ["Lattice length", lattice.length],
                    ["Cell length", cell.length],
                    ["Number of cells", len(lattice.children)],
                    ["Bends per cells", n_bends],
                    ["Reverse bends per cells", n_reverse_bends],
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
                    ["Qₓ", twiss.tune_x],
                    # TODO: fix chroma in apace
                    # ["Chromaticity x", twiss.chromaticity_x],
                    ["βₓ,ₘₐₓ / m", np.max(twiss.beta_x)],
                    ["βₓ,ₘᵢₙ / m", np.min(twiss.beta_x)],
                    ["βₓ,ₘₑₐₙ / m", np.mean(twiss.beta_x)],
                    ["ηₓ,ₘₐₓ / m", np.max(twiss.eta_x)],
                ],
                [
                    ["Qᵧ", twiss.tune_y],
                    # TODO: fix chroma in apace
                    # ["Chromaticity y", twiss.chromaticity_y],
                    ["βᵧ,ₘₐₓ / m", np.max(twiss.beta_y)],
                    ["βᵧ,ₘᵢₙ / m", np.min(twiss.beta_y)],
                    ["βᵧ,ₘₑₐₙ / m", np.mean(twiss.beta_y)],
                    ["ηᵧ,ₘₐₓ / m", 0],
                ],
                [
                    ["Mom. compaction", twiss.alpha_c],
                    ["Emittance", twiss.emittance_x],
                    ["I₁", twiss.i1],
                    ["I₂", twiss.i2],
                    ["I₃", twiss.i3],
                    ["I₄", twiss.i4],
                    ["I₅", twiss.i5],
                ],
            ],
        ],
        [
            "Floor plan",
            ["floor_plan_cell.svg"],
        ],
    ]


def twiss_plot(twiss: ap.Twiss):
    from math import log10, floor
    from apace.plot import plot_twiss, draw_elements, draw_sub_lattices

    factor = np.max(twiss.beta_x) / np.max(twiss.eta_x)
    eta_x_scale = 10 ** floor(log10(factor))
    cell = twiss.lattice.children[0]
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    ax.set_xlim(0, cell.length)
    plot_twiss(ax, twiss, scales={"eta_x": eta_x_scale})
    draw_elements(ax, cell, labels=cell.length < 30)
    draw_sub_lattices(ax, cell)
    # draw_elements(ax, cell, labels=cell.length < 30, location="bottom")
    # draw_sub_lattices(ax, cell, location="top")
    ax.grid(axis="y", linestyle="--")
    plt.legend(
        bbox_to_anchor=(0, 1.05, 1, 0.2),
        loc="lower left",
        mode="expand",
        ncol=3,
        frameon=False,
    )
    fig.tight_layout()

    return fig


def floor_plan_plot(lattice: ap.Lattice):
    from apace.plot import floor_plan

    # fig_ring, ax = plt.subplots()
    # ax.axis("off")
    # floor_plan(ax, lattice, labels=False)

    fig_cell, ax = plt.subplots(figsize=FIG_SIZE)
    ax.axis("off")
    cell = lattice.children[0]
    floor_plan(ax, cell)
    return fig_cell
