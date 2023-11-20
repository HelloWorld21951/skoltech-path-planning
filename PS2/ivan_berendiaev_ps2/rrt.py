from typing import List, Callable

import numpy as np

from environment import State, ManipulatorEnv
from angle_util import angle_linspace


class RRTPlanner:
    def __init__(
        self, env: ManipulatorEnv, distance_fn: Callable, max_angle_step: float = 10.0
    ):
        """
        :param env: manipulator environment
        :param distance_fn: function distance_fn(state1, state2) -> float
        :param max_angle_step: max allowed step for each joint in degrees
        """
        self._env = env
        self._distance_fn = distance_fn
        self._max_angle_step = max_angle_step
        self._N = 1000000
        self._G = {}

    def sample(self):
        return np.array(
            [
                np.random.choice(
                    np.arange(-180, 180, 10),
                )
                for i in range(4)
            ]
        )

    def plan(self, start_state: State, goal_state: State) -> List[State]:
        self._G[start_state] = None
        for i in range(self._N):
            pass
        pass
