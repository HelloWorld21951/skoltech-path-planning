from typing import Generic, List

from states.states import State
from collision_checkers.collision_checker_interface import CollisionChecker
from state_spaces.state_space_interface import StateSpace
from planners.path import Path


class PathPlanner(Generic[State]):
    def __init__(self, state_space: StateSpace, collision_checker: CollisionChecker) -> None:
        self._state_space = state_space
        self._start_state = None
        self._goal_states = None
        self._collision_checker = collision_checker
        self._plan = []

    def _is_goal_reached(self, state: State):
        return state in self._goal_states

    def set_start_state(self, state: State) -> None:
        self._start_state = state

    def set_goal_states(self, states: List[State]) -> None:
        self._goal_states = states

    def plan(self) -> Path:
        raise NotImplementedError(f"Method plan() for class {self.__class__} is not implemented")
