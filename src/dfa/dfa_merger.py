from typing import Dict, Set, Tuple
from src.automata.state import State
from src.dfa.dfa import DFA


class DFAMerger:
    def __init__(self, A: DFA, B: DFA):
        self.A = A
        self.B = B

    def merge(self) -> DFA:
        self.A.extend_alphabet(self.B.alphabet)
        self.B.extend_alphabet(self.A.alphabet)

        new_start = State()
        new_states: Set[State] = set([new_start])
        new_accept_states: Set[State] = set(
            [new_start]) if self._is_accept((self.A.start_state, self.B.start_state)) else set()
        new_transition_function: Dict[Tuple[State, str], State] = {}

        explored: Set[Tuple[State, State]] = set()
        equivalences = {(self.A.start_state, self.B.start_state): new_start}

        searching = [(self.A.start_state, self.B.start_state)]

        while searching:
            state_pair = searching.pop()
            explored.add(state_pair)

            for symbol in self.A.alphabet:
                next_state_pair = (
                    self.A.transition_function[(state_pair[0], symbol)],
                    self.B.transition_function[(state_pair[1], symbol)],
                )

                if next_state_pair not in equivalences:
                    new_state = State()
                    equivalences[next_state_pair] = new_state
                    if next_state_pair not in explored:
                        searching.append(next_state_pair)

                from_state = equivalences[state_pair]
                to_state = equivalences[next_state_pair]

                new_states.add(to_state)
                if self._is_accept(next_state_pair):
                    new_accept_states.add(to_state)

                new_transition_function[(from_state, symbol)] = to_state

        return DFA(new_start, new_states, new_transition_function, new_accept_states, self.A.alphabet)

    def _is_accept(self, states: Tuple[State, State]) -> bool:
        return states[0] in self.A.accept_states or states[1] in self.B.accept_states
