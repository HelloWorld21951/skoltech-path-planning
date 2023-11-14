from typing import Generic
from functools import cached_property

from states.states import State
from spaces.space_interface import Space, StateSpace


class CollisionChecker(Generic[State]):
    def __init__(self, space: Space) -> None:
        self._cspace = self.make_configuration_space(space)

    @cached_property
    def cspace(self) -> StateSpace:
        return self._cspace

    def is_collision(self, state: State) -> bool:
        raise NotImplementedError(
            f"Collision checking for {self.__class__} class is not implemented"
        )

    def make_configuration_space(self, space: Space) -> StateSpace:
        raise NotImplementedError(
            f"Creation of configuration space for {self.__class__} class is not implaemented"
        )
