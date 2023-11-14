import numpy as np
from typing import Generic, Any, TypeVar

Space = TypeVar("Space")


class Workspace(Generic[Space]):
    def __init__(self, space: Space) -> None:
        self._space = space

    @property
    def space(self) -> Any:
        return self._space


class WorkspaceNumpyArray(Workspace[np.ndarray]):
    def __init__(self, space: np.ndarray) -> None:
        super().__init__(space)
