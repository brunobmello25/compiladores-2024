from src.automata.automata import Automata


def test_init_automata():
    got = Automata()

    assert got.states == []
    assert got.alphabet == []
    assert got.transition_function == {}
    assert got.start_state is None
    assert got.accept_states == []


def test_add_state():
    a1 = Automata()
    a2 = Automata()

    got1 = a1.add_state(False)
    got2 = a1.add_state(False)
    got3 = a1.add_state(True)
    got4 = a2.add_state(True)
    got5 = a2.add_state(False)

    assert got1 == "q0"
    assert got2 == "q1"
    assert got3 == "q2"
    assert got4 == "q3"
    assert got5 == "q4"

    assert a1.states == ["q0", "q1", "q2"]
    assert a1.accept_states == ["q2"]

    assert a2.states == ["q3", "q4"]
    assert a2.accept_states == ["q3"]
