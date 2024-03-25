
class Automata:
    def __init__(self):
        self.states = []
        self.alphabet = []
        self.transitions = {}
        self.initial_state = None
        self.final_states = []
        self.state_counter = 0

    def add_state(self):
        new_state = f'q{self.state_counter}'
        self.state_counter += 1
        self.states.append(new_state)
        return new_state
