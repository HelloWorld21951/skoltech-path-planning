from typing import Generic, List

from states.states import State


class Path(Generic[State]):
    def __init__(self) -> None:
        self._path = List[State]
        self._cost = 0.0

    @property
    def path(self) -> List[State]:
        return self._path

    @property
    def cost(self) -> float:
        return self._cost
