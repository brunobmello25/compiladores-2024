from typing import Tuple, Dict, Set

from src.automata.state import State
from src.utils.symbol import Symbol


class Automata:
    def __init__(self):
        self.start_state: State = State()
        self.states: Set[State] = {self.start_state}
        self.accept_states: Set[State] = {self.start_state}
        self.transition_function: Dict[
            Tuple[State, str | None], Set[State]
        ] = {}

    def symbol_set(self):
        return {
            symbol for (_, symbol) in self.transition_function.keys() if symbol
        }

    @staticmethod
    def make_shortcut_automata(shortcut: Symbol) -> "Automata":
        a = Automata()

        q0 = a.accept_states.pop()

        q1 = a.add_state(True)

        for ch in shortcut.shortcut_to_list():
            a.add_transition(q0, q1, ch)

        return a

    @staticmethod
    def make_symbol_automata(symbol: str) -> "Automata":
        a = Automata()

        q0 = a.accept_states.pop()

        q1 = a.add_state(True)
        a.add_transition(q0, q1, symbol)
        return a

    def epsilon_closure(self, state: State):
        closure = set([state])
        queue = [state]
        while queue:
            current = queue.pop(0)
            # Pegar todos os estados alcançáveis por ε-transições
            next_states = self.transition_function.get((current, None), [])
            for next_state in next_states:
                if next_state not in closure:
                    closure.add(next_state)
                    queue.append(next_state)
        return closure

    def __str__(self):
        output = ""

        output += f"Start State: {self.start_state.name}\n\n"

        output += "States: "
        output += ", ".join(sorted(state.name for state in self.states))
        output += "\n"

        output += "\nAccept States: "
        output += ", ".join(sorted(state.name for state in self.accept_states))
        output += "\n"

        output += "\nTransitions:\n"
        output += "\n".join(
            f"  {
                start.name} --[{symbol if symbol is not None else 'ε'}]--> {end.name}"
            for (start, symbol), ends in self.transition_function.items()
            for end in ends
        )

        return output

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
