from ingameleader.model.side import Side


DUST2_MAP_ID = 1

MAP = {
    "id": DUST2_MAP_ID,
    "name": "Dust 2",
    "ugly_name": "de_dust2"
}

T_START = 1
CT_START = 2
BOMBSITE_A = 3
BOMBSITE_B = 4
OUTSIDE_TUNNEL = 5
UPPER_TUNNEL = 6
TUNNEL_STAIRS = 7
LOWER_TUNNEL = 8
MID_DOORS = 9
MIDDLE = 10
B_DOORS = 11
OUTSIDE_LONG = 12
LONG_DOORS = 13
A_RAMP = 14
LONG_A = 15
EXTENDED_A = 16
TOP_OF_MID = 17
CATWALK = 18
SHORT_STAIRS = 19
UNDER_A = 20
PIT = 21

LOCATIONS = [
    {
        "id": T_START,
        "map_id": DUST2_MAP_ID,
        "name": "tstart",
        "x": 395,
        "y": 917,
    },
    {
        "id": OUTSIDE_TUNNEL,
        "map_id": DUST2_MAP_ID,
        "name": "outsidetunnel",
        "x": 185,
        "y": 680,
    },
    {
        "id": UPPER_TUNNEL,
        "map_id": DUST2_MAP_ID,
        "name": "uppertunnel",
        "x": 185,
        "y": 490,
    },
    {
        "id": BOMBSITE_B,
        "map_id": DUST2_MAP_ID,
        "name": "bombsiteb",
        "x": 210,
        "y": 135,
    },
    {
        "id": TUNNEL_STAIRS,
        "map_id": DUST2_MAP_ID,
        "name": "tunnelstairs",
        "x": 310,
        "y": 470,
    },
    {
        "id": LOWER_TUNNEL,
        "map_id": DUST2_MAP_ID,
        "name": "lowertunnel",
        "x": 370,
        "y": 405,
    },
    {
        "id": MID_DOORS,
        "map_id": DUST2_MAP_ID,
        "name": "middoors",
        "x": 467,
        "y": 365,
    },
    {
        "id": MIDDLE,
        "map_id": DUST2_MAP_ID,
        "name": "middle",
        "x": 460,
        "y": 240,
    },
    {
        "id": B_DOORS,
        "map_id": DUST2_MAP_ID,
        "name": "bdoors",
        "x": 264,
        "y": 232,
    },
    {
        "id": OUTSIDE_LONG,
        "map_id": DUST2_MAP_ID,
        "name": "outsidelong",
        "x": 655,
        "y": 745,
    },
    {
        "id": LONG_DOORS,
        "map_id": DUST2_MAP_ID,
        "name": "longdoors",
        "x": 710,
        "y": 620,
    },
    {
        "id": A_RAMP,
        "map_id": DUST2_MAP_ID,
        "name": "aramp",
        "x": 890,
        "y": 150,
    },
    {
        "id": LONG_A,
        "map_id": DUST2_MAP_ID,
        "name": "longa",
        "x": 880,
        "y": 380,
    },
    {
        "id": BOMBSITE_A,
        "map_id": DUST2_MAP_ID,
        "name": "bombsitea",
        "x": 820,
        "y": 170,
    },
    {
        "id": EXTENDED_A,
        "map_id": DUST2_MAP_ID,
        "name": "extendeda",
        "x": 660,
        "y": 170,
    },
    {
        "id": TOP_OF_MID,
        "map_id": DUST2_MAP_ID,
        "name": "topofmid",
        "x": 530,
        "y": 640,
    },
    {
        "id": CATWALK,
        "map_id": DUST2_MAP_ID,
        "name": "catwalk",
        "x": 520,
        "y": 475,
    },
    {
        "id": SHORT_STAIRS,
        "map_id": DUST2_MAP_ID,
        "name": "shortstairs",
        "x": 630,
        "y": 355,
    },
    {
        "id": CT_START,
        "map_id": DUST2_MAP_ID,
        "name": "ctstart",
        "x": 625,
        "y": 210,
    },
    {
        "id": UNDER_A,
        "map_id": DUST2_MAP_ID,
        "name": "undera",
        "x": 720,
        "y": 230,
    },
    {
        "id": PIT,
        "map_id": DUST2_MAP_ID,
        "name": "pit",
        "x": 885,
        "y": 630,
    },
]

T_RUSH_A_LONG = 1
T_SPLIT_A = 2
T_RUSH_B = 3
T_MID_TO_B = 4
CT_2A_2B_1MID = 5
CT_RUSH_A_LONG = 6

EXEMPLAR_ROUTES = [
    {
        "strategy_id": T_RUSH_B,
        "_locations": [
            T_START,
            OUTSIDE_TUNNEL,
            UPPER_TUNNEL,
            BOMBSITE_B
        ]
    },
    {
        "strategy_id": T_MID_TO_B,
        "_locations": [
            T_START,
            OUTSIDE_TUNNEL,
            UPPER_TUNNEL,
            TUNNEL_STAIRS,
            LOWER_TUNNEL,
            MID_DOORS,
            MIDDLE,
            B_DOORS,
            BOMBSITE_B
        ]
    },
    {
        "strategy_id": T_RUSH_A_LONG,
        "_locations": [
            T_START,
            OUTSIDE_LONG,
            LONG_DOORS,
            LONG_A,
            A_RAMP,
            BOMBSITE_A,
        ]
    },
    {
        "strategy_id": T_SPLIT_A,
        "_locations": [
            T_START,
            OUTSIDE_LONG,
            TOP_OF_MID,
            CATWALK,
            SHORT_STAIRS,
            EXTENDED_A,
            BOMBSITE_A
        ]
    },
    {
        "strategy_id": T_SPLIT_A,
        "_locations": [
            T_START,
            OUTSIDE_LONG,
            LONG_DOORS,
            LONG_A,
            A_RAMP,
            BOMBSITE_A
        ]
    },
    {
        "strategy_id": CT_2A_2B_1MID,
        "_locations": [
            CT_START,
            MIDDLE,
            B_DOORS,
            BOMBSITE_B,
        ]
    },
    {
        "strategy_id": CT_2A_2B_1MID,
        "_locations": [
            CT_START,
            UNDER_A,
            LONG_A,
        ]
    },
    {
        "strategy_id": CT_RUSH_A_LONG,
        "_locations": [
            CT_START,
            UNDER_A,
            LONG_A,
            LONG_DOORS
        ]
    },
]

EXEMPLAR_ROUTES = [
    route for route in EXEMPLAR_ROUTES
]
# TODO Make this mapping somehow
ROUTES_TO_LOCATIONS = [
    route for route in EXEMPLAR_ROUTES
]

STRATEGIES = [
    # T Side strategies
    {
        "id": T_RUSH_A_LONG,
        "map_id": DUST2_MAP_ID,
        "name": "Rush A long",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.T.name,
    },
    {
        "id": T_SPLIT_A,
        "map_id": DUST2_MAP_ID,
        "name": "Split A",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.T.name,
    },
    {
        "id": T_RUSH_B,
        "map_id": DUST2_MAP_ID,
        "name": "Rush B",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.T.name,
    },
    {
        "id": T_MID_TO_B,
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
        "id": CT_2A_2B_1MID,
        "map_id": DUST2_MAP_ID,
        "name": "Two B, one mid, two A",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.CT.name,
    },
    {
        "id": CT_RUSH_A_LONG,
        "map_id": DUST2_MAP_ID,
        "name": "Rush A long",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.CT.name,
    },
]
