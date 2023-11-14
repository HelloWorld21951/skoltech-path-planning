from dataclasses import dataclass, field
from typing import TypeVar, Tuple
import numpy as np

State = TypeVar("State")


class Position2D(object):
    def __init__(self, x, y, theta) -> None:
        self._x = x
        self._y = y
        self._theta = theta

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def theta(self) -> int:
        return self._theta

    @classmethod
    def from_np_array(cls, np_array: np.ndarray):
        assert (
            np_array.shape == (3, 1),
            f"Can't create Position2D object from numpy array with shape {np_array.shape}, (3, 1) or (3, ) is "
            f"required",
        )
        return cls(np_array[0, 0], np_array[1, 0], np_array[2, 0])

    def to_numpy_array(self) -> np.ndarray:
        return np.array([[self.x], [self.y], [self.theta]])

    def to_tuple(self) -> Tuple[int]:
        return (self.x, self.y, self.theta)


@dataclass(order=True)
class PrioritizedState:
    priority: int
    state: State = field(compare=False)


class Position2DDiscreteTheta(Position2D):
    def __init__(self, x: int, y: int, theta: int) -> None:
        super().__init__(x, y, theta)

    @staticmethod
    def min_theta() -> int:
        return 0

    @staticmethod
    def max_theta() -> int:
        return 3
