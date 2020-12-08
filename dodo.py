from pathlib import Path
from operator import itemgetter

from scripts import info, lattices_generated_dir, simulation_elegant_dir

base_dir = Path(__file__).parent

# TODO: what does "clean" do???


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
            "name": f"{lattice['namespace']}/{lattice['name']}",
            "actions": [
                f"elegant {run_file} -macro=energy={energy},lattice={lattice_file},filename={target} > /dev/null"
            ],
            "targets": [target],
            "file_dep": [run_file, lattice_file],
            "clean": True,
        }


def task_lattice_info():
    from scripts import results_dir, info_file
    import json

    def save_data(path, data):
        path.write_text(data)
        return None

    for lattice in info["lattices"]:
        namespace, name = itemgetter("namespace", "name")(lattice)
        target = results_dir / namespace / name / "index.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        data = json.dumps(lattice)

        yield {
            "name": f"{lattice['namespace']}/{lattice['name']}",
            "actions": [(save_data, (target, data))],
            "targets": [target],
            "file_dep": [info_file],
            "clean": True,
        }


def task_elegant_results():
    from scripts import results_dir
    from scripts.data_elegant import results

    for lattice in lattices["elegant"]:
        namespace, name = itemgetter("namespace", "name")(lattice)
        output_dir = results_dir / namespace / name / "elegant"
        targets = [
            output_dir / "twiss_tables.json",
            output_dir / "twiss.svg",
            output_dir / "chroma.svg",
        ]
        twi_file = (simulation_elegant_dir / namespace / name).with_suffix(".twi")
        yield {
            "name": f"{lattice['namespace']}/{lattice['name']}",
            "actions": [(results, (lattice, output_dir))],
            "targets": targets,
            "file_dep": [twi_file],
            "clean": True,
        }
