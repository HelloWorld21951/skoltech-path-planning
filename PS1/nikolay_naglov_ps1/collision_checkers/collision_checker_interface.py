from typing import Generic
from functools import cached_property

from agents.agents import Agent
from spaces.spaces import Workspace
from states.states import State


class CollisionChecker(Generic[State]):
    def __init__(self, space: Workspace, agent: Agent) -> None:
        self._cspace = self.make_configuration_space(space, agent)

    @cached_property
    def cspace(self) -> Workspace:
        return self._cspace

    def is_collision(self, state: State) -> bool:
        raise NotImplementedError(
            f"Collision checking for {self.__class__} class is not implemented"
        )

    def make_configuration_space(self, space: Workspace, agent: Agent) -> Workspace:
        raise NotImplementedError(
            f"Creation of configuration space for {self.__class__} class is not implaemented"
        )
