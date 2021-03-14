from ingameleader.model.side import Side
from ingameleader.utils import format_location


INFERNO_MAP_ID = 2

MAP = {
    "id": INFERNO_MAP_ID,
    "name": "Inferno",
    "ugly_name": "de_inferno"
}
T_START = 22
CT_START = 23
BOMBSITE_A = 24
BOMBSITE_B = 25
LOWER_MID = 26
T_RAMP = 27
BANANA = 28
SECOND_MID = 29
MIDDLE = 30
TOP_OF_MID = 31
ARCH = 32
BALCONY = 33
BACK_ALLEY = 34
LIBRARY = 35
APARTMENTS = 36
RUINS = 37
QUAD = 38

LOCATIONS = [
    {
        "id": T_START,
        "map_id": INFERNO_MAP_ID,
        "name": "tstart",
        "x": 95,
        "y": 690,
    },
    {
        "id": CT_START,
        "map_id": INFERNO_MAP_ID,
        "name": "ctstart",
        "x": 917,
        "y": 353,
    },
    {
        "id": BOMBSITE_A,
        "map_id": INFERNO_MAP_ID,
        "name": "bombsitea",
        "x": 830,
        "y": 705,
    },
    {
        "id": BOMBSITE_B,
        "map_id": INFERNO_MAP_ID,
        "name": format_location("Bombsite B"),
        "x": 500,
        "y": 225,
    },
    {
        "id": LOWER_MID,
        "map_id": INFERNO_MAP_ID,
        "name": format_location("Lower Mid"),
        "x": 272,
        "y": 760,
    },
    {
        "id": T_RAMP,
        "map_id": INFERNO_MAP_ID,
        "name": format_location("T Ramp"),
        "x": 412,
        "y": 618,
    },
    {
        "id": BANANA,
        "map_id": INFERNO_MAP_ID,
        "name": format_location("Banana"),
        "x": 487,
        "y": 432,
    },
    {
        "id": SECOND_MID,
        "map_id": INFERNO_MAP_ID,
        "name": format_location("Second Mid"),
        "x": 425,
        "y": 815,
    },
    {
        "id": MIDDLE,
        "map_id": INFERNO_MAP_ID,
        "name": format_location("Middle"),
        "x": 500,
        "y": 670,
    },
    {
        "id": TOP_OF_MID,
        "map_id": INFERNO_MAP_ID,
        "name": format_location("Top of Mid"),
        "x": 715,
        "y": 680,
    },
    {
        "id": ARCH,
        "map_id": INFERNO_MAP_ID,
        "name": format_location("Arch"),
        "x": 800,
        "y": 500,
    },
    {
        "id": BACK_ALLEY,
        "map_id": INFERNO_MAP_ID,
        "name": format_location("Back Alley"),
        "x": 605,
        "y": 880,
    },
    {
        "id": LIBRARY,
        "map_id": INFERNO_MAP_ID,
        "name": format_location("Library"),
        "x": 950,
        "y": 540,
    },
    {
        "id": APARTMENTS,
        "map_id": INFERNO_MAP_ID,
        "name": format_location("Apartments"),
        "x": 675,
        "y": 855,
    },
    {
        "id": RUINS,
        "map_id": INFERNO_MAP_ID,
        "name": format_location("Ruins"),
        "x": 700,
        "y": 210,
    },
    {
        "id": QUAD,
        "map_id": INFERNO_MAP_ID,
        "name": format_location("Quad"),
        "x": 715,
        "y": 800,
    },
    {
        "id": BALCONY,
        "map_id": INFERNO_MAP_ID,
        "name": format_location("Balcony"),
        "x": 848,
        "y": 830,
    },
]

T_SECOND_MID_TO_A = 7
T_SECOND_MID_TO_B = 8
T_RUSH_APARTMENTS = 9
T_RUSH_B = 10
CT_2B_3A = 11
CT_RUSH_MIDDLE = 12

EXEMPLAR_ROUTES = [
    # T Side routes
    {
        "strategy_id": T_SECOND_MID_TO_A,
        "_locations": [
            T_START,
            LOWER_MID,
            SECOND_MID,
            MIDDLE,
            TOP_OF_MID,
            BOMBSITE_A
        ]
    },
    {
        "strategy_id": T_SECOND_MID_TO_B,
        "_locations": [
            T_START,
            LOWER_MID,
            SECOND_MID,
            MIDDLE,
            TOP_OF_MID,
            ARCH,
            CT_START,
            RUINS,
            BOMBSITE_B,
        ]
    },
    {
        "strategy_id": T_RUSH_APARTMENTS,
        "_locations": [
            T_START,
            LOWER_MID,
            SECOND_MID,
            BACK_ALLEY,
            APARTMENTS,
            BALCONY,
            BOMBSITE_A,
        ]
    },
    {
        "strategy_id": T_RUSH_B,
        "_locations": [
            T_START,
            LOWER_MID,
            T_RAMP,
            BANANA,
            BOMBSITE_B,
        ]
    },
    # CT Side routes
    # --- CT_2B_3A B routes
    {
        "strategy_id": CT_2B_3A,
        "_locations": [
            CT_START,
            RUINS,
        ]
    },
    {
        "strategy_id": CT_2B_3A,
        "_locations": [
            CT_START,
            RUINS,
            BOMBSITE_B
        ]
    },
    # --- CT_2B_3A A routes
    {
        "strategy_id": CT_2B_3A,
        "_locations": [
            CT_START,
            ARCH,
            TOP_OF_MID,
        ]
    },
    {
        "strategy_id": CT_2B_3A,
        "_locations": [
            CT_START,
            ARCH,
            TOP_OF_MID,
            QUAD,
        ]
    },
    {
        "strategy_id": CT_2B_3A,
        "_locations": [
            CT_START,
            LIBRARY,
            BOMBSITE_A,
            BALCONY,
            APARTMENTS,
        ]
    },
    {
        "strategy_id": CT_2B_3A,
        "_locations": [
            CT_START,
            LIBRARY,
            BOMBSITE_A,
            QUAD,
        ]
    },
    {
        "strategy_id": CT_2B_3A,
        "_locations": [
            CT_START,
            LIBRARY,
            BOMBSITE_A,
            TOP_OF_MID,
        ]
    },
    {
        "strategy_id": CT_2B_3A,
        "_locations": [
            CT_START,
            ARCH,
            BOMBSITE_A,
            BALCONY,
            APARTMENTS,
        ]
    },
    # CT_RUSH_MID
    {
        "strategy_id": CT_RUSH_MIDDLE,
        "_locations": [
            CT_START,
            ARCH,
            TOP_OF_MID,
            MIDDLE,
        ]
    },
]

STRATEGIES = [
    # T Side strategies
    {
        "id": T_SECOND_MID_TO_A,
        "map_id": INFERNO_MAP_ID,
        "name": "Second mid to A",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.T.name,
    },
    {
        "id": T_SECOND_MID_TO_B,
        "map_id": INFERNO_MAP_ID,
        "name": "Second mid to B",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.T.name,
    },
    {
        "id": T_RUSH_APARTMENTS,
        "map_id": INFERNO_MAP_ID,
        "name": "Rush Apartments",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.T.name,
    },
    {
        "id": T_RUSH_B,
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
        "id": CT_2B_3A,
        "map_id": INFERNO_MAP_ID,
        "name": "2 B, 1 A",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.CT.name,
    },
    {
        "id": CT_RUSH_MIDDLE,
        "map_id": INFERNO_MAP_ID,
        "name": "Rush middle",
        "alpha": 2,
        "beta": 2,
        "wins": 0,
        "losses": 0,
        "side": Side.CT.name,
    },
]
