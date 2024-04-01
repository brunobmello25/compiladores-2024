from src.automata.automata import Automata


def test_init_graph():
    got = Automata()

    assert got.states == []
    assert got.alphabet == []
    assert got.transitions == {}
    assert got.initial_state is None
    assert got.final_states == []


def test_add_state():
    a1 = Automata()
    a2 = Automata()

    a1.add_state(False)
    a1.add_state(False)
    a1.add_state(True)
    a2.add_state(True)
    a2.add_state(False)

    assert len(a1.states) == 3
    assert len(a2.states) == 2
    assert a1.states[0].name == "q0"
    assert a1.states[1].name == "q1"
    assert a1.states[2].name == "q2"
    assert a2.states[0].name == "q3"
    assert a2.states[1].name == "q4"
