class State:
    def __init__(self, name, final):
        self.name = name
        self.final = final


class Automata:
    def __init__(self):
        self.states = []
        self.alphabet = []
        self.transitions = {}
        self.initial_state = None
        self.final_states = []
        self.state_counter = 0

    def add_state(self, final):
        new_name = f'q{self.state_counter}'
        self.state_counter += 1

        state = State(new_name, final)

        self.states.append(state)
        return state
