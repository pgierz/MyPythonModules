import simulation_tools

test_simulation = simulation_tools.cosmos_simulation("pgierz@stan1:/ace/user/pgierz/cosmos-aso-wiso/LIG-Tx10")


def test_names():
    assert test_simulation.user == "pgierz"
    assert test_simulation.host == "stan1"
    assert test_simulation.path == "/ace/user/pgierz/cosmos-aso-wiso/LIG-Tx10"
    assert test_simulation.expid == "LIG-Tx10"
