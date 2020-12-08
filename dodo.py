from pathlib import Path
from operator import itemgetter

from scripts import (
    info,
    info_file,
    results_dir,
    lattices_generated_dir,
    simulation_elegant_dir,
)

base_dir = Path(__file__).parent

# TODO:
# * what does "clean" do???
# * define task dependencies
# * define all task


lattices = {}
for lattice in info["lattices"]:
    for simulation_program in lattice["simulations"]:
        try:
            lattices[simulation_program].append(lattice)
        except KeyError:
            lattices[simulation_program] = [lattice]


def task_elegant_twiss_simulation():
    for lattice in lattices["elegant"]:
        namespace, name, energy = itemgetter("namespace", "name", "energy")(lattice)
        run_file = base_dir / "elegant" / "twiss.ele"
        lattice_file = (lattices_generated_dir / namespace / name).with_suffix(".lte")
        target = (simulation_elegant_dir / namespace / name).with_suffix(".twi")
        target.parent.mkdir(parents=True, exist_ok=True)
        yield {
            "name": f"{namespace}/{name}",
            "actions": [
                f"elegant {run_file} -macro=energy={energy},lattice={lattice_file},filename={target} > /dev/null"
            ],
            "targets": [target],
            "file_dep": [run_file, lattice_file],
            "clean": True,
        }


def task_index_json():
    def save_data(path, data):
        path.write_text(data)
        return None

    import json

    target = results_dir / "index.json"
    yield {
        "name": "index.json",
        "actions": [(save_data, (target, json.dumps(info)))],
        "targets": [target],
        "file_dep": [info_file],
    }


def task_lattice_info():
    "simalar to task_index_json, but info file per lattice"

    def save_data(path, data):
        path.write_text(data)
        return None

    import json

    for lattice in info["lattices"]:
        namespace, name = itemgetter("namespace", "name")(lattice)
        target = results_dir / namespace / name / "index.json"
        target.parent.mkdir(parents=True, exist_ok=True)

        yield {
            "name": f"{namespace}/{name}",
            "actions": [(save_data, (target, json.dumps(lattice)))],
            "targets": [target],
            "file_dep": [info_file],
            "clean": True,
        }


def task_elegant_results():
    from scripts.data_elegant import results

    for lattice in lattices["elegant"]:
        namespace, name = itemgetter("namespace", "name")(lattice)
        output_dir = results_dir / namespace / name / "elegant"
        targets = [
            output_dir / path
            for path in [
                "twiss_tables.json",
                "twiss.svg",
                "chroma.svg",
            ]
        ]
        twi_file = (simulation_elegant_dir / namespace / name).with_suffix(".twi")
        yield {
            "name": f"{namespace}/{name}",
            "actions": [(results, (lattice, output_dir))],
            "targets": targets,
            "file_dep": [twi_file],
            "clean": True,
        }


def task_madx_results():
    from scripts.data_madx import results

    for lattice in lattices["madx"]:
        namespace, name = itemgetter("namespace", "name")(lattice)
        output_dir = results_dir / namespace / name / "madx"
        targets = [
            output_dir / path
            for path in [
                "twiss_tables.json",
                "twiss.svg",
            ]
        ]
        lattice_file = (lattices_generated_dir / namespace / name).with_suffix(".madx")
        yield {
            "name": f"{namespace}/{name}",
            "actions": [(results, (lattice, output_dir))],
            "targets": targets,
            "file_dep": [lattice_file],
            "clean": True,
        }


def task_apace_results():
    from scripts.data_madx import results

    for lattice in lattices["madx"]:
        namespace, name = itemgetter("namespace", "name")(lattice)
        output_dir = results_dir / namespace / name / "apace"
        targets = [
            output_dir / path
            for path in [
                "twiss_tables.json",
                "twiss.svg",
                "floor_plan_ring.svg",
                "floor_plan_cell.svg",
            ]
        ]
        lattice_file = (lattices_generated_dir / namespace / name).with_suffix(".json")
        yield {
            "name": f"{namespace}/{name}",
            "actions": [(results, (lattice, output_dir))],
            "targets": targets,
            "file_dep": [lattice_file],
            "clean": True,
        }
