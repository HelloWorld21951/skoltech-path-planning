from typing import Generic

from states.states import State


class Action(Generic[State]):
    def __init__(self) -> None:
        pass

    def apply(self, state: State) -> State:
        raise NotImplementedError(
            f"Applying action for {self.__class__} is not implemented"
        )

    def cost(self) -> int:
        raise NotImplementedError(
            f"Action cost for {self.__class__} is not implemented"
        )
