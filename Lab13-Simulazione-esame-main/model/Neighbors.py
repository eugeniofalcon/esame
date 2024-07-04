from dataclasses import dataclass
from datetime import datetime

@dataclass
class Neighbor:
    state1: str
    state2: str

    def __str__(self):
        return f"State {self.state1} neighboor to state {self.state2}"

    def __hash__(self):
        return hash((self.state1, self.state2))
