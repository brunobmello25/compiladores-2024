from typing import Dict, Set, Tuple
from src.automata.state import State
from src.dfa.dfa import DFA


class DFAMerger:
    def __init__(self, A: DFA, B: DFA):
        self.A = A
        self.B = B
        self.new_start = State()
        self.new_states: Set[State] = set([self.new_start])
        self.new_accept_states: Set[State] = set()
        self.new_transition_function: Dict[Tuple[State, str], State] = {}

        self.A.extend_alphabet(self.B.alphabet)
        self.B.extend_alphabet(self.A.alphabet)

    def merge(self) -> DFA:
        explored: Set[Tuple[State, State]] = set()

        equivalences = {
            (self.A.start_state, self.B.start_state): self.new_start}

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

                    self.process_accept_state_priorities(
                        next_state_pair, equivalences)

                    if next_state_pair not in explored:
                        searching.append(next_state_pair)

                from_state = equivalences[state_pair]
                to_state = equivalences[next_state_pair]

                self.new_states.add(to_state)
                if self._is_accept(next_state_pair):
                    self.new_accept_states.add(to_state)

                self.new_transition_function[(from_state, symbol)] = to_state

        return DFA(self.new_start, self.new_states, self.new_transition_function, self.new_accept_states, self.A.alphabet)

    def process_accept_state_priorities(self, current_state: Tuple[State, State], equivalences: Dict[Tuple[State, State], State]):
        if not self._is_accept(current_state):
            return

        is_A_accept = current_state[0] in self.A.accept_states
        is_B_accept = current_state[1] in self.B.accept_states

        if not is_A_accept or not is_B_accept:
            equivalent_state = equivalences[current_state]
            if is_A_accept:
                equivalent_state.token_type = current_state[0].token_type
                equivalent_state.token_priority = current_state[0].token_priority
            else:
                equivalent_state.token_type = current_state[1].token_type
                equivalent_state.token_priority = current_state[1].token_priority
            return

        a_priority = current_state[0].token_priority
        b_priority = current_state[1].token_priority

        if a_priority is None or b_priority is None:
            raise RuntimeError("Illegal State: Both token priorities must be set. Token {} has priority {} and token {} has priority {}".format(
                current_state[0], a_priority, current_state[1], b_priority))

        if a_priority > b_priority:
            equivalent_state = equivalences[current_state]
            equivalent_state.token_type = current_state[0].token_type
            equivalent_state.token_priority = current_state[0].token_priority
        elif a_priority < b_priority:
            equivalent_state = equivalences[current_state]
            equivalent_state.token_type = current_state[1].token_type
            equivalent_state.token_priority = current_state[1].token_priority
        else:
            raise RuntimeError("Illegal State: Both token priorities must be different. Token {} has priority {} and token {} has priority {}".format(
                current_state[0].token_type, a_priority, current_state[1].token_type, b_priority))

    def _is_accept(self, states: Tuple[State, State]) -> bool:
        return states[0] in self.A.accept_states or states[1] in self.B.accept_states
