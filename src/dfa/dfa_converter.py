from collections import deque
from typing import FrozenSet
from src.automata.automata import Automata
from src.automata.state import State
from src.dfa.dfa import DFA


class DFAConverter:
    def __init__(self, nfa: Automata):
        self.nfa = nfa
        self.states = set()
        self.transition_function = {}
        self.start_state = self._epsilon_closure(frozenset([nfa.start_state]))
        self.accept_states = set()

        if any(state in nfa.accept_states for state in self.start_state):
            self.accept_states.add(self.start_state)

        self._build()

    def get_dfa(self) -> DFA:
        equivalences = {}
        for state in self.states:
            equivalences[state] = State()

        new_start = equivalences[self.start_state]
        new_states = set(equivalences[state] for state in self.states)
        new_accept_states = set(equivalences[state]
                                for state in self.accept_states)
        new_transition_function = {
            (equivalences[start], symbol): equivalences[end] for (start, symbol), end in self.transition_function.items()
        }

        new_alphabet = {
            symbol for (_, symbol) in self.transition_function.keys() if symbol is not None
        }

        return DFA(new_start, new_states, new_transition_function, new_accept_states, new_alphabet)

    def _epsilon_closure(self, states: FrozenSet[State]) -> FrozenSet[State]:
        closure = set()
        for state in states:
            closure.update(self.nfa.epsilon_closure(state))
        return frozenset(closure)

    def _build(self):
        queue = deque([self.start_state])
        self.states.add(self.start_state)

        while queue:
            current = queue.popleft()
            for symbol in self.nfa.symbol_set():
                next_states = self._move(current, symbol)
                next_state_closure = self._epsilon_closure(next_states)

                if next_state_closure not in self.states:
                    self.states.add(next_state_closure)
                    queue.append(next_state_closure)

                self.transition_function[(
                    current, symbol)] = next_state_closure

                if any(state in self.nfa.accept_states for state in next_state_closure):
                    self.accept_states.add(next_state_closure)

    def _move(self, states: FrozenSet[State], symbol: str) -> FrozenSet[State]:
        result = set()
        for state in states:
            transition_key = (state, symbol)
            if transition_key in self.nfa.transition_function:
                result.update(self.nfa.transition_function[transition_key])
        return frozenset(result)

    def print(self):
        print("States:", ", ".join(["{" + ", ".join(state.name for state in s) +
              "}" for s in sorted(self.states, key=lambda x: sorted(y.name for y in x))]))
        print(
            "Start State: {" + ", ".join(state.name for state in self.start_state) + "}")
        print("Accept States:", ", ".join(["{" + ", ".join(state.name for state in s) + "}" for s in sorted(
            self.accept_states, key=lambda x: sorted(y.name for y in x))]))
        print("Transitions:")
        for (start_states, symbol), end_states in self.transition_function.items():
            start_names = "{" + \
                ", ".join(state.name for state in start_states) + "}"
            end_names = "{" + \
                ", ".join(state.name for state in end_states) + "}"
            print(f"  {start_names} --[{symbol}]--> {end_names}")
