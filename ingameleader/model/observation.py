from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from ingameleader.model.side import Side
from ingameleader.model.context import Context


@dataclass
class Observation:
    location: Optional[str]
    ct_score: Optional[int]
    t_score: Optional[int]
    time: Optional[timedelta]
    side: Optional[Side]
    money: Optional[int]
    context: Context

    @property
    def round_number(self):
        round_number = self.ct_score + self.t_score if self.ct_score is not None and self.t_score is not None else None
        if round_number is None:
            return None
        if round_number > 30 or round_number < 0:
            return None
        return  round_number
