from typing import Generic, List

from states.states import State


class Path(Generic[State]):
    def __init__(self, path: List[State], cost: int) -> None:
        self._path = path
        self._cost = cost

    @property
    def path(self) -> List[State]:
        return self._path

    @property
    def cost(self) -> int:
        return self._cost

    def to_list_of_tuples(self):
        return [state.to_tuple() for state in self._path]
