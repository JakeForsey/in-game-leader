from ingameleader.model.side import Side


DUST2_MAP_ID = 1

MAP = {
    "id": DUST2_MAP_ID,
    "name": "Dust 2",
}

STRATEGIES = [
    # T Side strategies
    {
        "map_id": DUST2_MAP_ID,
        "name": "A long",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.T.name,
    },
    {
        "map_id": DUST2_MAP_ID,
        "name": "Split A",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.T.name,
    },
    {
        "map_id": DUST2_MAP_ID,
        "name": "B tunnels",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.T.name,
    },
    {
        "map_id": DUST2_MAP_ID,
        "name": "Mid to B",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.T.name,
    },
    # CT Side strategies
    {
        "map_id": DUST2_MAP_ID,
        "name": "2 B, 1 mid, 2 A",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.CT.name,
    },
    {
        "map_id": DUST2_MAP_ID,
        "name": "Rush A long",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.CT.name,
    },
]
