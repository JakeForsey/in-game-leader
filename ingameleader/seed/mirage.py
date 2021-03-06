from ingameleader.model.side import Side


MIRAGE_MAP_ID = 3

MAP = {
    "id": MIRAGE_MAP_ID,
    "name": "Mirage",
}

STRATEGIES = [
    # T Side strategies
    {
        "map_id": MIRAGE_MAP_ID,
        "name": "Mid to B",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.T.name,
    },
    {
        "map_id": MIRAGE_MAP_ID,
        "name": "Mid to A",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.T.name,
    },
    {
        "map_id": MIRAGE_MAP_ID,
        "name": "Slow A",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.T.name,
    },
    {
        "map_id": MIRAGE_MAP_ID,
        "name": "Rush A",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.T.name,
    },
    {
        "map_id": MIRAGE_MAP_ID,
        "name": "Rush B",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.T.name,
    },
    # CT Side strategies
    {
        "map_id": MIRAGE_MAP_ID,
        "name": "2 B, 1 mid, 2 A",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.CT.name,
    },
    {
        "map_id": MIRAGE_MAP_ID,
        "name": "Rush ramp",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.CT.name,
    },
]
