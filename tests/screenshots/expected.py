from datetime import timedelta
from ingameleader.app import Observation, Context, format_location, Side


EXPECTED_OBSERVATIONS = {
    "tests/screenshots/1613854227.6711657.png": Observation(
        location=None,
        ct_score=None,
        t_score=None,
        time=None,
        side=None,
        money=2850,
        context=Context.DEAD
    ),
    "tests/screenshots/1613854507.9261875.png": Observation(
        location=format_location("B Doors"),
        ct_score=5,
        t_score=4,
        time=timedelta(seconds=107),
        side=None,
        money=3050,
        context=Context.ALIVE
    ),
    "tests/screenshots/1613854648.0500681.png": Observation(
        context=Context.BETWEEN_ROUNDS,
        location=None,
        ct_score=7,
        t_score=4,
        time=None,
        side=None,
        money=5650,
        winner=Side.CT,
    ),
    # TODO uncomment once we have context recognition for warm up
    # "tests/screenshots/1613856369.744595.png": Observation(
    #     location=None,
    #     ct_score=0,
    #     t_score=0,
    #     time=None,
    #     side=None,
    #     money=16000,
    #     context=Context.WARM_UP
    # )
    "tests/screenshots/1613856429.811474.png": Observation(
        location=format_location("Apartments"),
        ct_score=0,
        t_score=0,
        time=timedelta(seconds=89),
        side=None,
        money=500,
        context=Context.ALIVE
    ),
    "tests/screenshots/1613856409.782785.png": Observation(
        location=format_location("Lower Mid"),
        ct_score=0,
        t_score=0,
        time=timedelta(seconds=109),
        side=None,
        money=500,
        context=Context.ALIVE
    ),
    "tests/screenshots/1613858922.2529435.png": Observation(
        location=format_location("Ruins"),
        ct_score=12,
        t_score=10,
        time=timedelta(seconds=53),
        side=None,
        money=4500,
        context=Context.ALIVE
    ),
    "tests/screenshots/1613859963.2744315.png": Observation(
        location=format_location("CT STart"),
        ct_score=0,
        t_score=0,
        time=timedelta(seconds=114),
        side=Side.CT,
        money=500,
        context=Context.ALIVE
    ),
    "tests/screenshots/1613856529.9070535.png": Observation(
        location=format_location("T Ramp"),
        ct_score=1,
        t_score=0,
        time=timedelta(seconds=106),
        side=None,
        money=2800,
        context=Context.ALIVE
    ),
    # Counter Terrorist win between rounds
    "tests/screenshots/1613858091.4364786.png": Observation(
        location=None,
        ct_score=7,
        t_score=8,
        time=None,
        side=None,
        money=5150,
        context=Context.BETWEEN_ROUNDS,
        winner=Side.CT,
    ),
    "tests/screenshots/1613858441.821546.png": Observation(
        location=format_location("CT Start"),
        ct_score=10,
        t_score=8,
        time=timedelta(seconds=92),
        side=None,
        money=1500,
        context=Context.ALIVE,
    ),
    # Terrorist win between rounds
    "tests/screenshots/1613857600.9269984.png": Observation(
        location=None,
        ct_score=6,
        t_score=4,
        time=None,
        side=None,
        money=6100,
        context=Context.BETWEEN_ROUNDS,
        winner=Side.T
    ),
}
