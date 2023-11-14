import numpy as np

from functools import cached_property
from typing import Any, Generic, TypeVar

AgentType = TypeVar("AgentType")


class Agent(Generic[AgentType]):
    def __init__(self, config: AgentType):
        self._config = config

    @cached_property
    def config(self) -> AgentType:
        return self._config


class AgentNumpyArray(Agent[np.ndarray]):
    def __init__(self, config: np.ndarray):
        super().__init__(config)
