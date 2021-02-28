from dataclasses import dataclass


@dataclass
class Strategy:
    strategy_id: str
    strategy_name: str
    alpha: int = 2
    beta: int = 2
    wins: int = 0
    losses: int = 0


@dataclass
class StrategeyUpdate:
    strategy_id: str
    win: bool
