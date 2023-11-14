from typing import Generic, List, Any

from states.states import State


class Space(object):
    def __init__(self, space: Any) -> None:
        self._space = space

    @property
    def space(self) -> Any:
        return self._space


class StateSpace(Generic[State], Space):
    def __init__(self, state_space: List[State]) -> None:
        super().__init__(state_space)
