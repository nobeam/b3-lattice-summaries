from scripts import test_output_dir


def test_results(test_lattice):
    from scripts.data_elegant import results

    results(test_lattice, test_output_dir / "elegant")
