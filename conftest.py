import pytest


@pytest.fixture(scope="session")
def test_lattice():
    from scripts import info

    namespace = "kuske"
    name = "bessy3_5ba-20p_v_reference"
    for lattice in info["lattices"]:
        if lattice["name"] == name and lattice["namespace"] == namespace:
            return lattice
