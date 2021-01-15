import json
from operator import itemgetter

import numpy as np

import matplotlib.pyplot as plt
from eleganttools import SDDS, draw_elements

from . import simulation_elegant_dir, FIG_SIZE


def results(lattice, output_dir):
    output_dir.mkdir(exist_ok=True, parents=True)
    name, namespace = itemgetter("name", "namespace")(lattice)
    print(f"\033[1m[elegant] Generating results for {namespace}/{name}\033[0m")

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
    return [
        [
            "Global Machine & Lattice Parameter",
            [
                [
                    ["Energy / MeV", data["pCentral"] / 3913.90152459 * 2],
                    ["Natural Emittance / rad m", data["ex0"]],
                    ["U₀ / Mev", data["U0"]],
                    ["ɑ", data["alphac"]],
                    ["ɑ₂", data["alphac2"]],
                    ["Jᵟ", data["Jdelta"]],
                    ["τᵟ", data["taudelta"]],
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
                    ["Qₓ", data["nux"]],
                    ["dQₓ / dδ", data["dnux/dp"]],
                    ["d²Qₓ / dδ²", data["dnux/dp2"]],
                    ["d³Qₓ / dδ³", data["dnux/dp3"]],
                    ["βₓ,ₘₐₓ / m", data["betaxMax"]],
                    ["βₓ,ₘᵢₙ / m", data["betaxMin"]],
                    ["βₓ,ₘₑₐₙ / m", data["betaxAve"]],
                    ["ηₓ,ₘₐₓ / m", data["etaxMax"]],
                    ["Jₓ", data["Jx"]],
                    ["τₓ / s", data["taux"]],
                ],
                [
                    ["Qᵧ", data["nuy"]],
                    ["dQᵧ / dδ", data["dnuy/dp"]],
                    ["d²Qᵧ / dδ²", data["dnuy/dp2"]],
                    ["d³Qᵧ / dδ³", data["dnuy/dp3"]],
                    ["βᵧ,ₘₐₓ / m", data["betayMax"]],
                    ["βᵧ,ₘᵢₙ / m", data["betayMin"]],
                    ["βᵧ,ₘₑₐₙ / m", data["betayAve"]],
                    ["ηᵧ,ₘₐₓ / m", data["etayMax"]],
                    ["Jᵧ", data["Jy"]],
                    ["τᵧ / s", data["tauy"]],
                ],
            ],
        ],
        [
            "Chromaticity",
            ["chroma.svg"],
        ],
    ]


def twiss_plot(data):
    from math import floor, log10

    factor = np.max(data["betax"]) / np.max(data["etax"])
    eta_x_scale = 10 ** floor(log10(factor))
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    ax.plot(data["s"], data["betax"], "#EF4444", label=r"$\beta_x$ / m")
    ax.plot(data["s"], data["betay"], "#1D4ED8", label=r"$\beta_y$ / m")
    ax.plot(
        data["s"],
        eta_x_scale * data["etax"],
        "#10B981",
        label=rf"{eta_x_scale} $\eta_x$ / m",
    )
    ax.set_xlabel("position s / m")
    ax.grid(color="#E5E7EB", linestyle="--", linewidth=1)
    ax.set_xlim(0, 15)  # TODO: use cell length!
    draw_elements(ax, data, labels=True)
    plt.legend(
        bbox_to_anchor=(0, 1.05, 1, 0.2),
        loc="lower left",
        mode="expand",
        ncol=3,
        frameon=False,
    )
    fig.tight_layout()
    return fig


def chroma_plot(data):
    domain = -0.02, 0.02
    coef_x = (0, *itemgetter("dnux/dp", "dnux/dp2", "dnux/dp3")(data))
    coef_y = (0, *itemgetter("dnuy/dp", "dnuy/dp2", "dnuy/dp3")(data))
    chroma_x = np.polynomial.Polynomial(coef_x)
    chroma_y = np.polynomial.Polynomial(coef_y)
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    ax.plot(*chroma_x.linspace(domain=domain), label=r"$\nu_x$")
    ax.plot(*chroma_y.linspace(domain=domain), label=r"$\nu_y$")
    ax.set_xlabel(r"$\Delta p / p$")
    ax.grid(color="#E5E7EB", linestyle="--", linewidth=1)
    ax.legend()
    fig.tight_layout()
    return fig
