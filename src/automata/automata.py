from typing import List, Tuple, Dict, Set

from src.utils.symbol import Symbol


class Automata:
    state_counter = 0

    def __init__(self):
        self.states: List[str] = []
        self.alphabet: List[Symbol] = []
        self.start_state: str | None = None
        self.accept_states: List[str] = []
        self.current_state: str | None = None
        self.transition_function: Dict[Tuple[str, str], Set[str]] = {}

    def add_state(self, final: bool) -> str:
        new_state = f"q{Automata.state_counter}"
        Automata.state_counter += 1

        self.states.append(new_state)
        if final:
            self.accept_states.append(new_state)

        return new_state

    def add_transition(self, start: str, end: str, value: str):
        if (start, value) not in self.transition_function:
            self.transition_function[(start, value)] = set()
        self.transition_function[(start, value)].add(end)
