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
        if observation.side is not None:
            self.side = observation.side

    @property
    def complete(self):
        return self.ct_win or self.t_win

    @property
    def won(self) -> Optional[bool]:
        won = None
        if self.side == Side.CT:
            won = self.ct_win
        if self.side == Side.T:
            won = self.t_win
        return won
