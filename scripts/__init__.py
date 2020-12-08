from pathlib import Path

import tomlkit
from matplotlib import rcParams

rcParams["font.family"] = "sans-serif"
rcParams["font.sans-serif"] = ["Inter"]

base_dir = Path(__file__).parent.parent
results_dir = base_dir / "results"
results_dir.mkdir(exist_ok=True)
test_dir = base_dir / "tests"
test_output_dir = test_dir / "_output"
test_output_dir.mkdir(exist_ok=True)
summary_dir = results_dir / "summary"
summary_dir.mkdir(exist_ok=True)
templates_dir = base_dir / "templates"
lattices_dir = base_dir / "lattices"
lattices_generated_dir = lattices_dir / "_generated"
simulation_dir = base_dir / "_simulations"
simulation_elegant_dir = simulation_dir / "elegant"
elegant_dir = base_dir / "elegant"

info_file = lattices_dir / "info.toml"
info = tomlkit.loads(info_file.read_text())
