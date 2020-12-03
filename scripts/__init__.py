from pathlib import Path

import tomlkit

base_dir = Path(__file__).parent.parent
dist_dir = base_dir / "dist"
dist_dir.mkdir(exist_ok=True)
test_dir = base_dir / "tests"
test_output_dir = test_dir / "_output"
test_output_dir.mkdir(exist_ok=True)
summary_dir = dist_dir / "summary"
summary_dir.mkdir(exist_ok=True)
templates_dir = base_dir / "templates"
lattices_dir = base_dir / "lattices"
simulation_dir = base_dir / "_simulations"
simulation_elegant_dir = simulation_dir / "elegant"
elegant_dir = base_dir / "elegant"

info = tomlkit.loads((lattices_dir / "info.toml").read_text())
