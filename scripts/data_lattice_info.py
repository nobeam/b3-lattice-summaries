import json
from itertools import groupby
from operator import itemgetter

import latticejson
from latticejson.utils import flattened_element_sequence

from . import lattices_generated_dir


def all_equal(iterable):
    "Returns True if all the elements are equal to each other"
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


def results(lattice, output_dir):
    output_dir.mkdir(exist_ok=True, parents=True)
    name, namespace = itemgetter("name", "namespace")(lattice)
    lattice_path = (lattices_generated_dir / namespace / name).with_suffix(".json")
    lattice_dict = latticejson.load(lattice_path)
    elements = lattice_dict["elements"]
    ring = lattice_dict["lattices"][lattice_dict["root"]]
    ring_flattened = flattened_element_sequence(lattice_dict)
    circumference = sum(elements[name][1]["length"] for name in ring_flattened)
    is_fully_symmetric = all_equal(ring)
    table = [
        ["Energy / MeV", lattice["energy"]],
        ["Circumference / m", circumference],
        ["Fully symmetric", int(is_fully_symmetric)],
        ["Number of sections", len(ring)],
    ]
    if is_fully_symmetric:
        section_flattened = list(flattened_element_sequence(lattice_dict, ring[0]))
        section_length = sum(elements[name][1]["length"] for name in section_flattened)
        table.append(["Section length / m", section_length])
        bends = [name for name in section_flattened if elements[name][0] == "Dipole"]
        n_bends = sum(elements[name][1]["angle"] > 0 for name in bends)
        n_reverse_bends = len(bends) - n_bends
        table.append(["Bends per section", n_bends])
        table.append(["Reverse bends per section", n_reverse_bends])
        if "straight" in elements:
            straight_length = 2 * elements["straight"][1]["length"]
            table.append(["Straight length / m", straight_length])
            table.append(
                ["Free straight ratio", straight_length * len(ring) / circumference]
            )
    with (output_dir / "lattice_info.json").open("w") as file:
        json.dump(["Lattice Info", table], file)
