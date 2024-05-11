from typing import Dict, Tuple
import pytest

from src.automata.state import State
from src.dfa.dfa import DFA


@pytest.fixture
def simple_dfa():
    State.state_counter = 0

    # Set up a simple DFA
    q0 = State()
    q1 = State()
    q2 = State()
    states = {q0, q1, q2}
    transition_function: Dict[Tuple[State, str], State] = {
        (q0, 'a'): q1,
        (q1, 'b'): q2
    }
    accept_states = {q2}
    alphabet = {'a', 'b'}

    return DFA(start_state=q0, states=states, transition_function=transition_function, accept_states=accept_states, alphabet=alphabet)


def test_simple_backtrack(simple_dfa):
    State.state_counter = 0

    dfa = simple_dfa
    # Make some transitions
    dfa.transition('a')  # q0 -> q1
    dfa.transition('b')  # q1 -> q2
    assert dfa.current_state.name == 'q2'

    # Backtrack one step
    dfa.backtrack(1)
    assert dfa.current_state.name == 'q1'

    # Backtrack another step
    dfa.backtrack(1)
    assert dfa.current_state.name == 'q0'


def test_backtrack_too_many(simple_dfa):
    State.state_counter = 0

    dfa = simple_dfa
    # Make one transition
    dfa.transition('a')  # s0 -> s1

    # Attempt to backtrack more steps than the history size
    with pytest.raises(Exception, match="Cannot backtrack 2 steps"):
        dfa.backtrack(2)


def test_backtrack_zero_steps(simple_dfa):
    State.state_counter = 0

    dfa = simple_dfa
    # Make some transitions
    dfa.transition('a')  # s0 -> s1
    dfa.transition('b')  # s1 -> s2

    # Backtrack zero steps and check state remains the same
    dfa.backtrack(0)
    assert dfa.current_state.name == 'q2'
