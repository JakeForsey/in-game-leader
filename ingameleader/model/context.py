import enum


class Context(enum.Enum):
    ALIVE = 0
    DEAD = 1
    ROUND_WINNER_SCREEN = 2
    BUY_PHASE = 3
    WARM_UP = 4
    UNKNOWN = 5
