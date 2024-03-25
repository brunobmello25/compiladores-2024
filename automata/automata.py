
class Automata:
    def __init__(self):
        self.states = []
        self.alphabet = []
        self.transitions = {}
        self.initial_state = None
        self.final_states = []

    def add_state(self, state):
        self.states.append(state)
