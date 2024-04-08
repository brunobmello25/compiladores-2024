from collections import deque
from typing import Tuple, Dict, Set

from src.automata.state import State


class Automata:
    def __init__(self):
        self.start_state: State = State()
        self.states: Set[State] = {self.start_state}
        self.accept_states: Set[State] = {self.start_state}
        self.transition_function: Dict[
            Tuple[State, str | None], Set[State]
        ] = {}

    def print(self):
        # Print the start state
        print(f"Start State: {self.start_state.name}")

        # Print all states
        print("States:", ", ".join(state.name for state in self.states))

        # Print accept states
        print(
            "Accept States:",
            ", ".join(state.name for state in self.accept_states),
        )

        # Print the transition function
        print("Transitions:")
        for (start, symbol), ends in self.transition_function.items():
            symbol_display = (
                symbol if symbol is not None else "ε"
            )  # ε represents epsilon transitions
            for end in ends:
                print(f"  {start.name} --[{symbol_display}]--> {end.name}")

    def transitions_as_string(self) -> Dict[Tuple[str, str | None], Set[str]]:
        converted_dict = {
            (state.name, symbol): {s.name for s in state_set}
            for (state, symbol), state_set in self.transition_function.items()
        }

        return converted_dict

    def add_state(self, final: bool) -> State:
        new_state = State()

        self.states.add(new_state)
        if final:
            self.accept_states.add(new_state)

        return new_state

    def add_transition(self, start: State, end: State, symbol: str | None):
        if (start, symbol) not in self.transition_function:
            self.transition_function[(start, symbol)] = set()
        self.transition_function[(start, symbol)].add(end)

    @staticmethod
    def union(a1: "Automata", a2: "Automata") -> "Automata":
        automata = Automata()

        automata.states.update(a1.states, a2.states)
        automata.accept_states = a1.accept_states.union(a2.accept_states)
        automata.transition_function = (
            automata.transition_function
            | a1.transition_function
            | a2.transition_function
        )

        automata.add_transition(automata.start_state, a1.start_state, None)
        automata.add_transition(automata.start_state, a2.start_state, None)

        return automata

    def check_transition_by_state_name(
        self, start_name: str, end_name: str, symbol: str | None
    ) -> bool:
        for key, states in self.transition_function.items():
            if key[0].name == start_name and key[1] == symbol:
                for state in states:
                    if state.name == end_name:
                        return True
                break
        return False

    def optional(self):
        self.accept_states.add(self.start_state)

    def concat(self, a2: "Automata"):
        for state in self.accept_states:
            self.add_transition(state, a2.start_state, None)

        self.states.update(a2.states)
        self.accept_states = a2.accept_states
        self.transition_function = (
            self.transition_function | a2.transition_function
        )

    def plus(self):
        for state in self.accept_states:
            self.add_transition(state, self.start_state, None)

    def star(self):
        self.plus()
        self.accept_states.add(self.start_state)

    from collections import deque

    def to_dfa(self) -> "Automata":
        # Helper function to get epsilon closure of a set of states.
        # Epsilon closure includes the state itself and any state reachable through epsilon transitions.
        def epsilon_closure(states: Set[State]) -> Set[State]:
            closure = set(states)
            stack = list(states)
            while stack:
                state = stack.pop()
                for next_state in self.transition_function.get(
                    (state, None), []
                ):
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
            return closure

        # Helper function to move from a set of states with a given symbol.
        def move(states: Set[State], symbol: str) -> Set[State]:
            next_states = set()
            for state in states:
                next_states.update(
                    self.transition_function.get((state, symbol), [])
                )
            return epsilon_closure(next_states)

        dfa = Automata()
        state_map = {}  # Maps sets of NFA states to DFA states

        start_closure = epsilon_closure({self.start_state})
        state_map[frozenset(start_closure)] = dfa.start_state

        # Queue for BFS
        queue = deque([start_closure])

        while queue:
            current_states = queue.pop()
            current_dfa_state = state_map[frozenset(current_states)]

            for symbol in {
                s for _, s in self.transition_function if s is not None
            }:
                next_states = move(current_states, symbol)
                if not next_states:
                    continue

                if frozenset(next_states) not in state_map:
                    new_dfa_state = dfa.add_state(
                        final=any(s in self.accept_states for s in next_states)
                    )
                    state_map[frozenset(next_states)] = new_dfa_state
                    queue.appendleft(next_states)
                else:
                    new_dfa_state = state_map[frozenset(next_states)]

                dfa.add_transition(current_dfa_state, new_dfa_state, symbol)

        return dfa
