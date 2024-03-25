from automata import Automata


def test_init_graph():
    got = Automata()

    assert got.states == []
    assert got.alphabet == []
    assert got.transitions == {}
    assert got.initial_state is None
    assert got.final_states == []


def test_add_state():
    automata = Automata()

    got1 = automata.add_state()
    got2 = automata.add_state()
    got3 = automata.add_state()

    assert got1 == 'q0'
    assert got2 == 'q1'
    assert got3 == 'q2'
    assert automata.states == ['q0', 'q1', 'q2']
    assert automata.alphabet == []
    assert automata.transitions == {}
    assert automata.initial_state is None
    assert automata.final_states == []
