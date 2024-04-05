class State:
    state_counter = 0

    def __init__(self):
        self._create_name()

    def _create_name(self):
        self.name = f"q{State.state_counter}"
        State.state_counter += 1
