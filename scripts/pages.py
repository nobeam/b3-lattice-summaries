import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from . import info, templates_dir, dist_dir, summary_dir


def index():
    env = Environment(loader=FileSystemLoader(searchpath=templates_dir))
    template = env.get_template("index.html")
    (dist_dir / "index.html").write_text(template.render(info=info))


def elegant_summary():
    from eleganttools import SDDS

    env = Environment(loader=FileSystemLoader(searchpath=templates_dir))
    template = env.get_template("elegant_summary.html")

    for lattice in info["lattices"]:
        name = lattice["name"]
        output_dir = summary_dir / name / "elegant"
        twiss_tables = json.loads((output_dir / "twiss_tables.json").read_text())
        (output_dir / "index.html").write_text(
            template.render(
                lattice=lattice,
                twiss_tables=twiss_tables,
            )
        )
