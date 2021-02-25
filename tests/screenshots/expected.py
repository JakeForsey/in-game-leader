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
        location=format_location("B Doors"),
        ct_score=None,  # TODO switch this to 7 once we can
        t_score=4,
        time=None,
        side=None,
        money=5650,
        context=Context.ALIVE  # TODO switch this to between rounds once implemented
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
}
