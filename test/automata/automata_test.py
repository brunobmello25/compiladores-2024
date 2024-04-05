from src.automata.automata import Automata


def test_concat_empty_with_symbol():
    Automata.state_counter = 0
    empty = Automata()
    start_state = empty.add_state(True)
    empty.set_start(start_state)

    symbol_automata = make_basic_char_automata()

    empty.concat(symbol_automata)

    assert empty.states == ["q0", "q3", "q4"]
    assert empty.accept_states == ["q4"]
    assert empty.start_state == "q0"
    assert empty.transition_function[("q0", None)] == {"q3"}
    assert empty.transition_function[("q3", "a")] == {"q4"}
    assert len(empty.transition_function.keys()) == 2


def test_optional():
    Automata.state_counter = 0
    a = make_basic_char_automata()

    a.optional()

    assert a.states == ["q0", "q1"]
    assert a.accept_states == ["q1", "q0"]
    assert a.start_state == "q0"
    assert a.transition_function[("q0", "a")] == {"q1"}


def test_plus():
    Automata.state_counter = 0
    a = make_basic_char_automata()

    a.plus()

    assert a.states == ["q0", "q1"]
    assert a.start_state == "q0"
    assert a.accept_states == ["q1"]
    assert a.transition_function[("q0", "a")] == {"q1"}
    assert a.transition_function[("q1", None)] == {"q0"}
    assert len(a.transition_function.keys()) == 2


def test_star():
    Automata.state_counter = 0
    a = make_basic_char_automata()

    a.star()

    assert a.states == ["q0", "q1"]
    assert a.start_state == "q0"
    assert a.accept_states == ["q1", "q0"]
    assert a.transition_function[("q0", "a")] == {"q1"}
    assert a.transition_function[("q1", None)] == {"q0"}
    assert len(a.transition_function.keys()) == 2


def test_concat():
    # TODO: isso deveria estar em um beforeEach
    Automata.state_counter = 0
    a1 = Automata()
    q0 = a1.add_state(False)
    q1 = a1.add_state(False)
    q2 = a1.add_state(True)
    q3 = a1.add_state(False)
    q4 = a1.add_state(True)
    a1.add_transition(q0, q1, None)
    a1.add_transition(q1, q2, "a")
    a1.add_transition(q0, q3, None)
    a1.add_transition(q3, q4, "b")
    a1.set_start(q0)

    a2 = Automata()
    q5 = a2.add_state(False)
    q6 = a2.add_state(True)
    a2.add_transition(q5, q6, "c")
    a2.set_start(q5)

    a1.concat(a2)

    assert a1.states == ["q0", "q1", "q2", "q3", "q4", "q7", "q8"]
    assert a1.start_state == "q0"
    assert a1.accept_states == ["q8"]

    assert a1.transition_function[("q0", None)] == {"q1", "q3"}
    assert a1.transition_function[("q1", "a")] == {"q2"}
    assert a1.transition_function[("q3", "b")] == {"q4"}
    assert a1.transition_function[("q2", None)] == {"q7"}
    assert a1.transition_function[("q4", None)] == {"q7"}
    assert a1.transition_function[("q7", "c")] == {"q8"}
    assert len(a1.transition_function.keys()) == 6


def test_union():
    Automata.state_counter = 0
    a1 = make_basic_char_automata()

    a2 = Automata()
    q2 = a2.add_state(False)
    q3 = a2.add_state(True)
    a2.set_start(q2)
    a2.add_transition(q2, q3, "b")

    result = Automata.union(a1, a2)

    assert result.states == ["q4", "q5", "q6", "q7", "q8"]
    assert result.start_state == "q4"
    assert result.accept_states == ["q6", "q8"]
    assert result.transition_function[("q4", None)] == {"q5", "q7"}
    assert result.transition_function[("q5", "a")] == {"q6"}
    assert result.transition_function[("q7", "b")] == {"q8"}
    assert len(result.transition_function.keys()) == 3


def test_set_start():
    Automata.state_counter = 0
    a = Automata()
    a.add_state(False)
    a.add_state(True)
    a.add_state(False)

    assert a.start_state is None
    a.set_start("q1")
    assert a.start_state == "q1"


def test_init_automata():
    Automata.state_counter = 0
    got = Automata()

    assert got.states == []
    assert got.transition_function == {}
    assert got.start_state is None
    assert got.accept_states == []


def test_add_state():
    Automata.state_counter = 0
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


def test_add_transition():
    Automata.state_counter = 0
    a = Automata()
    a.add_state(False)
    a.add_state(True)
    a.add_state(False)

    a.add_transition("q0", "q1", "a")
    a.add_transition("q1", "q2", "1")
    a.add_transition("q1", "q0", "1")
    a.add_transition("q2", "q0", "[A-Z]")

    assert a.transition_function[("q0", "a")] == {"q1"}
    assert a.transition_function[("q1", "1")] == {"q2", "q0"}
    assert a.transition_function[("q2", "[A-Z]")] == {"q0"}


def make_basic_char_automata() -> Automata:
    a = Automata()
    q0 = a.add_state(False)
    q1 = a.add_state(True)
    a.set_start(q0)
    a.add_transition(q0, q1, "a")

    return a
