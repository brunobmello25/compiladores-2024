from typing import List

from src.utils.symbol import Symbol


class State:
    def __init__(self, name, final):
        self.name: str = name
        self.final: bool = final


class Automata:
    state_counter: int = 0

    def __init__(self):
        self.states: List[State] = []
        self.alphabet: List[Symbol] = []
        self.transitions: dict[tuple[State, Symbol], State] = {}
        self.initial_state: State | None = None
        self.final_states: List[State] = []

    def add_state(self, final):
        new_name = f"q{Automata.state_counter}"
        Automata.state_counter += 1

        state = State(new_name, final)

        self.states.append(state)
        return state
