
from typing import Dict, List,  Set, Tuple
from src.automata.state import State
from src.scanner.token_priority import TokenPriority


class DFA:
    def __init__(self, start_state: State, states: Set[State], transition_function: Dict[Tuple[State, str], State], accept_states: Set[State], alphabet: Set[str]):
        self.start_state = start_state
        self.transition_function = transition_function
        self.states = states
        self.accept_states = accept_states
        self.alphabet = alphabet
        self.current_state = start_state
        self.history: List[Tuple[State, str, State]] = []

    # TODO: convert to __str__
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

    def backtrack(self, amount: int):
        if amount > len(self.history):
            raise Exception(f"Cannot backtrack {amount} steps; only {
                            len(self.history)} moves recorded")

        # Perform the backtrack operation
        for _ in range(amount):
            start, _, _ = self.history.pop()
            self.current_state = start

    def transition(self, symbol: str) -> State:
        if (self.current_state, symbol) in self.transition_function:
            next_state = self.transition_function[(self.current_state, symbol)]
            self.history.append((self.current_state, symbol, next_state))
            self.current_state = next_state
            return self.current_state
        raise Exception(
            f"Invalid transition from {self.current_state.name} with symbol {symbol}")

    def is_accepting(self) -> bool:
        return self.current_state in self.accept_states

    def is_valid_transition(self, symbol: str) -> bool:
        return (self.current_state, symbol) in self.transition_function

    def get_accepting_state_info(self) -> Tuple[str, TokenPriority]:
        if not self.current_state in self.accept_states:
            raise Exception("Current state is not an accepting state")
        if self.current_state.token_type is None or self.current_state.token_priority is None:
            raise Exception("Current state does not have a token associated")

        return self.current_state.token_type, self.current_state.token_priority

    def reset(self):
        self.current_state = self.start_state
        self.history.clear()

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

    def associate_token(self, token_type: str, token_priority: TokenPriority = TokenPriority.LOW):
        for state in self.accept_states:
            state.token_type = token_type
            state.token_priority = token_priority

    def check(self, word: str) -> bool:
        accepts, _ = self.check_final_state(word)
        return accepts

    def check_final_state(self, word: str) -> Tuple[bool, State]:
        current_state = self.start_state

        for symbol in word:
            if (current_state, symbol) not in self.transition_function:
                return False, current_state
            current_state = self.transition_function[(current_state, symbol)]

        return current_state in self.accept_states, current_state
