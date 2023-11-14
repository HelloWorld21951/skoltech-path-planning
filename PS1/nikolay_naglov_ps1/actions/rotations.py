from actions.action_interface import Action
from states.states import Position2DDiscreteTheta


class Rotate(Action[Position2DDiscreteTheta]):
    def cost(self) -> int:
        return 1


class RotateCW(Rotate):
    def apply(self, state: Position2DDiscreteTheta) -> Position2DDiscreteTheta:
        new_theta = (
            state.theta - 1 if state.theta > state.min_theta() else state.max_theta()
        )
        return Position2DDiscreteTheta(state.x, state.y, new_theta)


class RotateCCW(Rotate):
    def apply(self, state: Position2DDiscreteTheta) -> Position2DDiscreteTheta:
        new_theta = (
            state.theta + 1 if state.theta < state.max_theta() else state.min_theta()
        )
        return Position2DDiscreteTheta(state.x, state.y, new_theta)
