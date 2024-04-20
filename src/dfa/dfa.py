
from typing import Dict, Set, Tuple
from src.automata.state import State


class DFA:
    def __init__(self, start_state: State, states: Set[State], transition_function: Dict[Tuple[State, str], State], accept_states: Set[State]):
        self.start_state = start_state
        self.transition_function = transition_function
        self.states = states
        self.accept_states = accept_states

    def print(self):
        print(f"Start State: {self.start_state.name}")

        print("States:", ", ".join(state.name for state in self.states))

        print("Accept States:", ", ".join(
            state.name for state in self.accept_states))

        print("Transitions:")
        for (start, symbol), end in self.transition_function.items():
            symbol_display = (
                symbol if symbol is not None else "ε"
            )
            print(f"  {start.name} --[{symbol_display}]--> {end.name}")

    def check(self, word: str) -> bool:
        current_state = self.start_state

        for symbol in word:
            if (current_state, symbol) not in self.transition_function:
                return False
            current_state = self.transition_function[(current_state, symbol)]

        return current_state in self.accept_states
