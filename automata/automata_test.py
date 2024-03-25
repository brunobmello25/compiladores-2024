from automata import Automata


def test_init_graph():
    got = Automata()

    assert got.states == []
    assert got.alphabet == []
    assert got.transitions == {}
    assert got.initial_state is None
    assert got.final_states == []


def test_add_state():
    got = Automata()

    got.add_state('q0')

    assert got.states == ['q0']
    assert got.alphabet == []
    assert got.transitions == {}
    assert got.initial_state is None
    assert got.final_states == []
