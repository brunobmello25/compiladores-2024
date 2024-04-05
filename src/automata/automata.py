from typing import List, Tuple, Dict, Set


class Automata:
    state_counter = 0

    def __init__(self):
        self.states: List[str] = []

        # TODO: tirar esse None e iniciar um automato com um estado
        self.start_state: str | None = None

        self.accept_states: List[str] = []
        self.transition_function: Dict[Tuple[str, str | None], Set[str]] = {}

    def add_state(self, final: bool) -> str:
        new_state = f"q{Automata.state_counter}"
        Automata.state_counter += 1

        self.states.append(new_state)
        if final:
            self.accept_states.append(new_state)

        return new_state

    def add_transition(self, start: str, end: str, symbol: str | None):
        if (start, symbol) not in self.transition_function:
            self.transition_function[(start, symbol)] = set()
        self.transition_function[(start, symbol)].add(end)

    def set_start(self, state: str):
        if state not in self.states:
            raise ValueError(f"State {state} does not exist")
        self.start_state = state

    def is_accept(self, state: str) -> bool:
        return state in self.accept_states

    @staticmethod
    def union(a1: "Automata", a2: "Automata") -> "Automata":
        a1_state_map = {}
        a2_state_map = {}

        a = Automata()

        start_state_union = a.add_state(False)
        a.set_start(start_state_union)

        for state in a1.states:
            new_state = a.add_state(a1.is_accept(state))
            a1_state_map[state] = new_state

        for state in a2.states:
            new_state = a.add_state(a2.is_accept(state))
            a2_state_map[state] = new_state

        for transition in a1.transition_function.keys():
            start, symbol = transition
            for end in a1.transition_function[transition]:
                a.add_transition(
                    a1_state_map[start], a1_state_map[end], symbol
                )

        for transition in a2.transition_function.keys():
            start, symbol = transition
            for end in a2.transition_function[transition]:
                a.add_transition(
                    a2_state_map[start], a2_state_map[end], symbol
                )

        a.add_transition(start_state_union, a1_state_map[a1.start_state], None)
        a.add_transition(start_state_union, a2_state_map[a2.start_state], None)

        return a

    def concat(self, a2: "Automata"):
        a2_state_map = {}

        original_accept_states = self.accept_states.copy()

        for state in a2.states:
            new_state = self.add_state(a2.is_accept(state))
            a2_state_map[state] = new_state

        for transition in a2.transition_function.keys():
            start, symbol = transition
            for end in a2.transition_function[transition]:
                self.add_transition(
                    a2_state_map[start], a2_state_map[end], symbol
                )

        for state in original_accept_states:
            self.add_transition(state, a2_state_map[a2.start_state], None)
            self.accept_states.remove(state)
