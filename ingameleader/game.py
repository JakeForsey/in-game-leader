from typing import Dict, Optional

from ingameleader.model.round import Round
from ingameleader.model.observation import Observation
from ingameleader.model.context import Context
from ingameleader.model.side import Side


class Game:
    def __init__(self):
        self.rounds: Dict[int, Round] = {}
        self.ct_score: int = 0
        self.t_score: int = 0
        self.side: Optional[Side] = None

    def update(self, observation: Observation):
        if observation.context != Context.ALIVE:
            return None

        if observation.round_number is None:
            return None

        if observation.round_number < max(self.rounds.keys(), default=-1):
            print("WARNING: Got an observation for an old round, ignoring!")
            return None
        if observation.round_number > max(self.rounds.keys(), default=99999) + 1:
            print("WARNING: Got an observation for a round much later in the game than expected, ignoring!")
            return None

        if observation.side is not None:
            self.side = observation.side

        current_round = self.rounds.get(observation.round_number, None)
        if current_round is not None:
            current_round.update(observation)

        else:
            current_round = Round(
                observation.round_number,
                side=observation.side,
                observations=[observation],
            )
            self.rounds[current_round.number] = current_round

            # The current round is the first one we have seen so update the
            # scores
            if len(self.rounds) == 1:
                self.ct_score = observation.ct_score
                self.t_score = observation.t_score

            last_round = self.rounds.get(current_round.number - 1, None)
            if last_round is not None:
                last_round.ct_win = self.ct_score < observation.ct_score
                last_round.t_win = not last_round.ct_win
                if last_round.ct_win:
                    self.ct_score += 1
                if last_round.t_win:
                    self.t_score += 1
                self.rounds[current_round.number - 1] = last_round

    @property
    def complete(self):
        return self.ct_score > 15 or self.t_score > 15 or self.t_score + self.ct_score > 30

    def __str__(self):
        return f"Game(rounds={self.rounds}, ct_score={self.ct_score}, t_score={self.t_score})"
