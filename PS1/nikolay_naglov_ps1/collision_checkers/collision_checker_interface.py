from typing import Generic

from states.states import State
from state_spaces.state_space_interface import StateSpace


class CollisionChecker(Generic[State]):
    def __init__(self, state_space: StateSpace) -> None:
        self._state_space = state_space

    def is_collision(self, state_1: State, state_2: State) -> bool:
        raise NotImplementedError(
            f"Collision checking for {self.__class__} class is not implemented"
        )
