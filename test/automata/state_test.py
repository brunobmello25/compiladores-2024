from src.automata.state import State


def test_state_name():
    q0 = State()
    q1 = State()

    assert q0.name == "q0"
    assert q1.name == "q1"
    assert State.state_counter == 2
