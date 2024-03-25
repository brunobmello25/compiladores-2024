from src.automata.automata import Automata, State


def test_init_graph():
    got = Automata()

    assert got.states == []
    assert got.alphabet == []
    assert got.transitions == {}
    assert got.initial_state is None
    assert got.final_states == []


def test_add_state():
    automata = Automata()

    got1 = automata.add_state(False)
    got2 = automata.add_state(False)
    got3 = automata.add_state(True)

    want1 = State('q0', False)
    want2 = State('q1', False)
    want3 = State('q2', True)

    assert got1.name == want1.name
    assert got2.name == want2.name
    assert got3.name == want3.name
    assert got1.final == want1.final
    assert got2.final == want2.final
    assert got3.final == want3.final

    assert automata.states == [got1, got2, got3]
