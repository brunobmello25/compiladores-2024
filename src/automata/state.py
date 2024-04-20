class State:
    state_counter = 0

    def __init__(self, ):
        self._create_name()
        self.token_type: str | None = None

    def _create_name(self):
        self.name = f"q{State.state_counter}"
        State.state_counter += 1
