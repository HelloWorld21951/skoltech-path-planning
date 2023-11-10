from typing import Generic, List
from functools import cached_property

from planners.path import State


class StateSpace(Generic[State]):
    def __init__(self) -> None:
        self._working_space = List[State]
        self._configuration_space = List[State]

    @cached_property
    def working_space(self) -> List[State]:
        return self._working_space

    @cached_property
    def configuration_space(self) -> List[State]:
        return self._configuration_space
