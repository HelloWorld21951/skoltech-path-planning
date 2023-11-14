import numpy as np
from scipy.signal import convolve2d

from agents.agents import AgentNumpyArray
from collision_checkers.collision_checker_interface import CollisionChecker
from spaces.spaces import WorkspaceNumpyArray
from states.states import Position2DDiscreteTheta
from utils.image_utils import normalize_image


class CollisionCheckerConvolve2D(CollisionChecker[Position2DDiscreteTheta]):
    def __init__(self, space: WorkspaceNumpyArray, agent: AgentNumpyArray) -> None:
        super().__init__(space, agent)

    def make_configuration_space(
        self, space: WorkspaceNumpyArray, agent: AgentNumpyArray
    ) -> WorkspaceNumpyArray:
        configuration_space = np.empty(
            (space.space.shape[0], space.space.shape[1], agent.config.shape[2])
        )
        agent_x_dim = int((agent.config.shape[0] - 1) / 2)
        agent_y_dim = int((agent.config.shape[1] - 1) / 2)
        for cfg_num in range(agent.config.shape[2]):
            configuration_space[:, :, cfg_num] = normalize_image(
                convolve2d(space.space, agent.config[:, :, cfg_num], "same", "symm")
            )
            configuration_space[:, :, cfg_num] = np.pad(
                configuration_space[
                    agent_x_dim:-agent_x_dim, agent_y_dim:-agent_y_dim, cfg_num
                ],
                (agent_x_dim, agent_y_dim),
                "constant",
                constant_values=1,
            )
        return configuration_space

    def is_collision(self, state: Position2DDiscreteTheta) -> bool:
        return self.cspace[state.x, state.y, state.theta] == 1
