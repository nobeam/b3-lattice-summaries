import json
from operator import itemgetter
import math

import numpy as np
from matplotlib import rcParams

rcParams["font.family"] = "sans-serif"
rcParams["font.sans-serif"] = ["Inter"]
import matplotlib.pyplot as plt
import tomlkit
from eleganttools import SDDS, draw_lattice, axis_labels

from . import info, summary_dir, elegant_dir, simulation_elegant_dir

tables_template = tomlkit.loads((elegant_dir / "twiss_tables.toml").read_text())


def main():
    lattices = info["lattices"]
    n_lattices = len(lattices)

    print(f"\033[1;36m[Generating elegant data 📈]\033[0m")
    for i, lattice in enumerate(lattices):
        name = lattice["name"]
        if "lte" not in lattice["formats"]:
            print(f"\033[1m[{i+1}/{n_lattices}] Skipping {name} (no lte file)\033[0m")
            continue

        output_dir = summary_dir / name / "elegant"
        output_dir.mkdir(exist_ok=True, parents=True)

        print(f"\033[1m[{i+1}/{n_lattices}] Building {name}\033[0m")
        twiss_data_path = (simulation_elegant_dir / name).with_suffix(".twi")
        twiss_data = SDDS(twiss_data_path).as_dict()

        # print(f"    Run elegant simulation ⚙️")

        print(f"    Generating tables 📝")
        with (output_dir / "twiss_tables.json").open("w") as file:
            json.dump(twiss_tables(twiss_data), file)

        print(f"    Generating twiss plot 📊")
        twiss_plot(twiss_data).savefig(output_dir / "twiss.svg")

        print(f"    Generate chroma plot 📊")
        chroma_plot(twiss_data).savefig(output_dir / "chroma.svg")


def twiss_tables(data):
    """Returns the relevant elgant data as dict"""
    data["energy"] = data["pCentral"] / 3913.90152459 * 2
    data["periodicity"] = math.nan
    data["cell_length"] = math.nan
    data["cell_angle"] = math.nan
    data["cell_angle_degree"] = math.nan
    data["circumference"] = math.nan
    return {
        table_name: [(name, data[key]) for name, key in table_template]
        for table_name, table_template in tables_template.items()
    }


def twiss_plot(data):
    eta_x_scale = 100
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(data["s"], data["betax"], "#EF4444")
    ax.plot(data["s"], data["betay"], "#1D4ED8")
    ax.plot(data["s"], eta_x_scale * data["etax"], "#10B981")
    ax.grid(color="#E5E7EB", linestyle="--", linewidth=1)
    draw_lattice(ax, data)
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
