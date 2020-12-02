from pathlib import Path

import numpy as np
from matplotlib import rcParams

rcParams["font.family"] = "sans-serif"
rcParams["font.sans-serif"] = ["Inter"]
import matplotlib.pyplot as plt

from eleganttools import SDDS, draw_lattice

from . import info, elegant_output_dir, summary_dir


def main():
    # for path in elegant_output_dir.rglob("*.twi"):
    for lattice in info["lattices"]:
        path = (elegant_output_dir / lattice["file"]).with_suffix(".twi")
        twiss = SDDS(path).as_dict()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(twiss["s"], twiss["betax"], "#EF4444")
        ax.plot(twiss["s"], twiss["betay"], "#1D4ED8")
        ax.plot(twiss["s"], 100 * twiss["etax"], "#10B981")
        ax.grid(color="#E5E7EB", linestyle="--", linewidth=1)
        draw_lattice(ax, twiss)
        fig.savefig((summary_dir / lattice["file"]).with_suffix(".svg"))


if __name__ == "__main__":
    main()