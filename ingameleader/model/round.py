from dataclasses import dataclass
from typing import List, Optional

from ingameleader.model.side import Side
from ingameleader.model.observation import Observation


@dataclass
class Round:
    number: int
    observations: List[Observation]
    side: Optional[Side] = None
    ct_win: bool = False
    t_win: bool = False

    def update(self, observation: Observation):
        self.observations.append(observation)
        self.side = observation.side

    @property
    def complete(self):
        return self.ct_win or self.t_win
