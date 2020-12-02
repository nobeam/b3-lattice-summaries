from pathlib import Path

import tomlkit

base_dir = Path(__file__).parent.parent
dist_dir = base_dir / "dist"
dist_dir.mkdir(exist_ok=True)
summary_dir = dist_dir / "summary"
summary_dir.mkdir(exist_ok=True)
templates_dir = base_dir / "templates"
lattices_dir = base_dir / "lattices"
elegant_output_dir = base_dir / "elegant_output"

info = tomlkit.loads((lattices_dir / "info.toml").read_text())
for lattice in info["lattices"]:
    lattice["name"] = lattice["file"].split(".")[0]
