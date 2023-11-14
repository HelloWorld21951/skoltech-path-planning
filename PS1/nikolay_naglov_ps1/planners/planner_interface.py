from typing import Generic, List, Union

from actions.action_interface import Action
from collision_checkers.collision_checker_interface import CollisionChecker
from states.path import Path
from spaces.spaces import Workspace
from states.states import State


class PathPlanner(Generic[State]):
    def __init__(self, collision_checker: CollisionChecker) -> None:
        self._collision_checker = collision_checker
        self._workspace = None
        self._start_state = None
        self._goal_state = None
        self._available_actions: List[Action] = []

    def _is_goal_reached(self, state: State) -> bool:
        return state in self._goal_states

    @property
    def start_state(self) -> Union[State, None]:
        return self._start_state

    @start_state.setter
    def start_state(self, state: State) -> None:
        self._start_state = state

    @property
    def goal_state(self) -> Union[State, None]:
        return self._goal_state

    @goal_state.setter
    def goal_state(self, state: State) -> None:
        self._goal_state = state

    @property
    def workspace(self) -> Union[Workspace, None]:
        return self._workspace

    @workspace.setter
    def workspace(self, workspace: Workspace) -> None:
        self._workspace = workspace

    @property
    def available_actions(self) -> List[Action]:
        return self._available_actions

    @available_actions.setter
    def available_actions(self, actions: List[Action]) -> None:
        self._available_actions = actions

    def plan(self) -> Path:
        raise NotImplementedError(
            f"Method plan() for class {self.__class__} is not implemented"
        )
