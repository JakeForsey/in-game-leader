from datetime import timedelta
from unittest import TestCase

from ingameleader.game import Game
from ingameleader.model.observation import Observation
from ingameleader.model.side import Side
from ingameleader.model.context import Context
from ingameleader.model.round import Round
from ingameleader.utils import format_location


class TestFrameToObservation(TestCase):
    def test_game_update_updates(self):
        game = Game()

        observation = Observation(
            context=Context.ALIVE,
            location=format_location("CT Start"),
            ct_score=0,
            t_score=0,
            time=timedelta(minutes=2),
            side=Side.CT,
            money=800,
            winner=None,
        )
        game.update(observation)
        assert game.t_score == 0
        assert game.ct_score == 0

        observation = Observation(
            context=Context.ALIVE,
            location=format_location("CT Start"),
            ct_score=1,
            t_score=0,
            time=timedelta(minutes=2),
            side=Side.CT,
            money=800,
            winner=None,
        )
        game.update(observation)
        assert game.t_score == 0
        assert game.ct_score == 1

        observation = Observation(
            context=Context.ALIVE,
            location=format_location("CT Start"),
            ct_score=1,
            t_score=1,
            time=timedelta(minutes=2),
            side=Side.CT,
            money=800,
            winner=None,
        )
        game.update(observation)
        assert game.t_score == 1
        assert game.ct_score == 1

        assert len(game.rounds) == 3

        assert isinstance(game.rounds[0], Round)
        assert game.rounds[0].ct_win
        assert not game.rounds[0].t_win
        assert game.rounds[0].side == Side.CT

        assert isinstance(game.rounds[1], Round)
        assert not game.rounds[1].ct_win
        assert game.rounds[1].t_win
        assert game.rounds[1].side == Side.CT
