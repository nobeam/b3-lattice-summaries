from scripts import test_output_dir


def test_results(test_lattice):
    from scripts.data_lattice_info import results

    results(test_lattice, test_output_dir / "lattice_info")
