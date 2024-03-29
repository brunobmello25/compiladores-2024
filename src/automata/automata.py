from typing import List

from src.utils.symbol import Symbol


class State:
    def __init__(self, name, final):
        self.name: str = name
        self.final: bool = final


class Automata:
    def __init__(self):
        self.states: List[State] = []
        self.alphabet: List[Symbol] = []
        self.transitions: dict[tuple[str, Symbol], str] = {}
        self.initial_state: str | None = None
        self.final_states: List[State] = []
        self.state_counter: int = 0

    def add_state(self, final) -> State:
        new_name = f"q{self.state_counter}"
        self.state_counter += 1

        state = State(new_name, final)

        self.states.append(state)
        return state

    def add_transition(self, origin: str, symbol: Symbol, destination: str):
        self.transitions[(origin, symbol)] = destination

    def set_initial_state(self, state: str):
        self.initial_state = state
