import json
from operator import itemgetter

import numpy as np

import matplotlib.pyplot as plt
from eleganttools import SDDS, draw_elements, axis_labels

from . import simulation_elegant_dir


def results(lattice, output_dir):
    namespace = lattice["namespace"]
    name = lattice["name"]
    print(f"\033[1mGenerating results for {namespace}/{name}\033[0m")

    output_dir.mkdir(exist_ok=True, parents=True)

    twiss_data_path = (simulation_elegant_dir / namespace / name).with_suffix(".twi")
    twiss_data = SDDS(twiss_data_path).as_dict()

    print(f"    Generating tables 📝")
    with (output_dir / "twiss_tables.json").open("w") as file:
        json.dump(twiss_tables(twiss_data), file)

    print(f"    Generating twiss plot 📊")
    twiss_plot(twiss_data).savefig(output_dir / "twiss.svg")

    print(f"    Generate chroma plot 📊")
    chroma_plot(twiss_data).savefig(output_dir / "chroma.svg")


def twiss_tables(data):
    """Returns the relevant elgant data as dict"""
    return [
        [
            "Global Machine & Lattice Parameter",
            [
                [
                    ["Energy / MeV", data["pCentral"] / 3913.90152459 * 2],
                    ["Cell length / m", 0],
                    ["Cell Angle / rad", 0],
                    ["Cell Angle / degree	", 0],
                    ["Circumference / m", 0],
                ],
                [
                    ["Natural Emittance / rad m", data["ex0"]],
                    ["Energy loss per turn $U_0$ / Mev", data["U0"]],
                    ["Momentum compaction $\\alpha_c$", data["alphac"]],
                    ["$\\alpha_{c2}$", data["alphac2"]],
                    ["$J_{\\delta}$", data["Jdelta"]],
                    ["$\\tau_{\\delta}$", data["taudelta"]],
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
                    ["$Q_x$", "nux"],
                    ["$dnux/dp$", "dnux/dp"],
                    ["$dnux/dp 2$", "dnux/dp2"],
                    ["$dnux/dp 3$", "dnux/dp3"],
                    ["max($\\beta_x$)", "betaxMax"],
                    ["min($\\beta_x$)", "betaxMin"],
                    ["mean($\\beta_x$)", "betaxAve"],
                    ["max($\\eta_x$)", "etaxMax"],
                    ["$J_x$", "Jx"],
                    ["$\\tau_x$", "taux"],
                ],
                [
                    ["$Q_y$", "nuy"],
                    ["$dnuy/dp$", "dnuy/dp"],
                    ["$dnuy/dp 2$", "dnuy/dp2"],
                    ["$dnuy/dp 3$", "dnuy/dp3"],
                    ["max($\\beta_y$)", "betayMax"],
                    ["min($\\beta_y$)", "betayMin"],
                    ["mean($\\beta_y$)", "betayAve"],
                    ["max($\\eta_y$)", "etayMax"],
                    ["$J_y$", "Jy"],
                    ["$\\tau_y$", "tauy"],
                ],
            ],
        ],
    ]


def twiss_plot(data):
    eta_x_scale = 100
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(data["s"], data["betax"], "#EF4444")
    ax.plot(data["s"], data["betay"], "#1D4ED8")
    ax.plot(data["s"], eta_x_scale * data["etax"], "#10B981")
    ax.grid(color="#E5E7EB", linestyle="--", linewidth=1)
    draw_elements(ax, data)
    axis_labels(ax, eta_x_scale=eta_x_scale)
    fig.tight_layout()
    return fig


def chroma_plot(data):
    domain = -0.02, 0.02
    coef_x = (0, *itemgetter("dnux/dp", "dnux/dp2", "dnux/dp3")(data))
    coef_y = (0, *itemgetter("dnuy/dp", "dnuy/dp2", "dnuy/dp3")(data))
    chroma_x = np.polynomial.Polynomial(coef_x)
    chroma_y = np.polynomial.Polynomial(coef_y)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(*chroma_x.linspace(domain=domain), label="nux")
    ax.plot(*chroma_y.linspace(domain=domain), label="nuy")
    ax.grid(color="#E5E7EB", linestyle="--", linewidth=1)
    ax.legend()
    return fig
