import enum


class Context(enum.Enum):
    ALIVE = 0
    DEAD = 1
    BETWEEN_ROUNDS = 2
    WARM_UP = 3
    UNKNOWN = 4
