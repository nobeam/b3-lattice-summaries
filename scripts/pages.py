from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from . import info, templates_dir, dist_dir, summary_dir, elegant_output_dir


def index():
    env = Environment(loader=FileSystemLoader(searchpath=templates_dir))
    template = env.get_template("index.html")
    (dist_dir / "index.html").write_text(template.render(info=info))


def summary():
    from eleganttools import SDDS

    env = Environment(loader=FileSystemLoader(searchpath=templates_dir))
    template = env.get_template("summary.html")

    for lattice in info["lattices"]:
        name = lattice["name"]
        data = SDDS((elegant_output_dir / name).with_suffix(".twi")).as_dict()
        # breakpoint()
        (summary_dir / name).with_suffix(".html").write_text(
            template.render(
                lattice=lattice,
                data=data,
                plot_path=(summary_dir / name).with_suffix(".svg"),
            )
        )
