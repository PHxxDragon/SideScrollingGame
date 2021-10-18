from typing import Dict


class State:
    """
    This is a prototype class for States.
    """
    def __init__(self):
        self.start_time: float = 0.0
        self.now: float = 0.0
        self.done: bool = False
        self.quit: bool = False
        self.next_state_name: str = None
        self.previous_state_name: str = None
        self.persist: Dict = {}

    def accept_events(self, events):
        """
        Processes events that were passed from the main event loop.
        """
        pass

    def startup(self, now, to_persist: Dict):
        """
        Add variables passed in persistant to the proper attributes and
        set the start time of the State to the current time.
        """
        self.persist = to_persist
        self.start_time = now

    def cleanup(self) -> Dict:
        """
        Reset State.done to False.
        Return persist dictionary
        """
        self.done = False
        return self.persist

    def update(self, now, mouse_pos, keyboard):
        """Update function for state."""
        pass

    def draw(self, surface, interpolate):
        """Draw function for state"""
        pass


class StateMachine:
    """
    A generic state machine.
    """
    def __init__(self):
        self.done = False
        self.state_dict: Dict[str, State] = {}
        self.state: State = None
        self.now = None

    def setup_state(self, state_dict: Dict[str, State], start_state: str) -> None:
        """
        Given a dictionary of states and a state to start in,
        creates the self.state_dict.
        """
        self.state_dict = state_dict
        self.state = state_dict[start_state]

    def update(self, now, mouse_pos, keyboard):
        """
        Checks if a state is done or has called for a game quit.
        State is flipped if neccessary and State.update is called.
        """
        self.now = now
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(now, mouse_pos, keyboard)

    def draw(self, surface, interpolate):
        self.state.draw(surface, interpolate)

    def flip_state(self):
        """
        When a State changes to done necessary startup and cleanup functions
        are called and the current State is changed.
        """
        previous_state_name = self.state.name
        state_name = self.state.next_state_name
        persist = self.state.cleanup()
        self.state = self.state_dict[state_name]
        self.state.startup(self.now, persist)
        self.state.previous = previous_state_name

    def accept_events(self, events):
        """
        Pass events down to current State.
        """
        self.state.accept_events(events)
