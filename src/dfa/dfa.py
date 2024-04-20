
from typing import Dict, Set, Tuple
from src.automata.state import State


class DFA:
    def __init__(self, start_state: State, states: Set[State], transition_function: Dict[Tuple[State, str], State], accept_states: Set[State], alphabet: Set[str]):
        self.start_state = start_state
        self.transition_function = transition_function
        self.states = states
        self.accept_states = accept_states
        self.alphabet = alphabet

    def print(self):
        print(f"Alphabet: {', '.join(sorted(self.alphabet))}")

        print(f"Start State: {self.start_state.name}")

        print("States:", ", ".join(sorted(state.name for state in self.states)))

        print("Accept States:", ", ".join(
            sorted(state.name for state in self.accept_states)))

        print("Transitions:")
        for (start, symbol), end in self.transition_function.items():
            symbol_display = (
                symbol if symbol is not None else "ε"
            )
            print(f"  {start.name} --[{symbol_display}]--> {end.name}")

    def extend_alphabet(self, new_alphabet: Set[str]):
        new_state = State()

        new_symbols = {
            symbol for symbol in new_alphabet if symbol not in self.alphabet}

        for new_symbol in new_symbols:
            for state in self.states:
                self.transition_function[(state, new_symbol)] = new_state

        new_alphabet = self.alphabet.union(new_symbols)

        for symbol in new_alphabet:
            self.transition_function[(new_state, symbol)] = new_state

        self.alphabet = new_alphabet
        self.states.add(new_state)

    def check(self, word: str) -> bool:
        current_state = self.start_state

        for symbol in word:
            if (current_state, symbol) not in self.transition_function:
                return False
            current_state = self.transition_function[(current_state, symbol)]

        return current_state in self.accept_states
