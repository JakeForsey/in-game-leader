from dataclasses import dataclass


@dataclass
class StrategyUpdate:
    strategy_id: str
    win: bool
