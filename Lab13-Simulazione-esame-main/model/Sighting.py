from dataclasses import dataclass
from datetime import datetime as dt

@dataclass
class Sighting:
    id: int
    datetime: dt
    city: str
    state: str
    country:str
    shape: str
    duration: int
    duration_hm: str
    comments: str
    date_posted: dt
    latitude: float
    longitude: float


    def __str__(self):
        return self.state

    def __hash__(self):
        return hash(self.id)