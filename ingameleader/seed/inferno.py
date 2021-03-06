from ingameleader.model.side import Side


INFERNO_MAP_ID = 2

MAP = {
    "id": INFERNO_MAP_ID,
    "name": "Inferno",
}

STRATEGIES = [
    # T Side strategies
    {
        "map_id": INFERNO_MAP_ID,
        "name": "Second mid to A",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.T.name,
    },
    {
        "map_id": INFERNO_MAP_ID,
        "name": "Second mid to B",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.T.name,
    },
    {
        "map_id": INFERNO_MAP_ID,
        "name": "Apartment rush",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.T.name,
    },
    {
        "map_id": INFERNO_MAP_ID,
        "name": "Rush B",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.T.name,
    },
    # CT Side strategies
    {
        "map_id": INFERNO_MAP_ID,
        "name": "2 B, 3 A",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.CT.name,
    },
    {
        "map_id": INFERNO_MAP_ID,
        "name": "Rush mid",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.CT.name,
    },
]
