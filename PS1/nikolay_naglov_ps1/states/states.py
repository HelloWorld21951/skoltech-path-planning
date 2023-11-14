from dataclasses import dataclass, field
from typing import TypeVar, Tuple

State = TypeVar("State")


@dataclass(order=True)
class PrioritizedState:
    priority: int
    state: State = field(compare=False)


@dataclass(eq=True, frozen=True)
class Position2D(object):
    x: int
    y: int
    theta: int

    def to_tuple(self) -> Tuple[int]:
        return (self.x, self.y, self.theta)


@dataclass(eq=True, frozen=True)
class Position2DDiscreteTheta(Position2D):
    @staticmethod
    def min_theta() -> int:
        return 0

    @staticmethod
    def max_theta() -> int:
        return 3
