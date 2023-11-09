import logging
import numpy as np
from typing import List


class State(object):
    def __init__(self) -> None:
        pass


class Action(object):
    def __init__(self) -> None:
        pass

    def apply(self, state: State) -> State:
        raise NotImplementedError(
            f"Applying action for {self.__class__} is not implemented"
        )


class Environment(object):
    def __init__(self) -> None:
        pass


class CollisionChecker(object):
    def __init__(self, environment: Environment) -> None:
        self._env = environment

    def is_collision(self, state_1: State, state_2: State) -> bool:
        raise NotImplementedError(
            f"Collision checking for {self.__class__} class is not implemented"
        )


class AStar(object):
    def __init__(self, collision_checker: CollisionChecker) -> None:
        self._start_state = None
        self._goal_states = None
        self._collision_checker = collision_checker
        self._plan = []
        self._cost_table = []
        self._visited = []
        self._parent_table = {}

    def set_start_state(self, state: State) -> None:
        self._start_state = state

    def set_goal_states(self, states: List[State]) -> None:
        self._goal_states = states

    def plan(self) -> List[State]:
        self._cleanup()
        pass

    def _cleanup(self) -> None:
        self._plan.clear()
        self._cost_table.clear()
        self._visited.clear()
        self._parent_table.clear()

    def h(self, state: State) -> int:
        raise NotImplementedError(
            f"Heuristic function for {self.__class__} class is not implemented"
        )
