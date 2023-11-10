from actions.action_interface import Action
from states.states import Position2DDiscreteTheta


class LinearMove(Action[Position2DDiscreteTheta]):
    def cost(self) -> int:
        return 1


class MoveUp(LinearMove):
    def apply(self, state: Position2DDiscreteTheta) -> Position2DDiscreteTheta:
        return Position2DDiscreteTheta(state.x, state.y + 1, state.theta)


class MoveDown(LinearMove):
    def apply(self, state: Position2DDiscreteTheta) -> Position2DDiscreteTheta:
        return Position2DDiscreteTheta(state.x, state.y - 1, state.theta)


class MoveLeft(LinearMove):
    def apply(self, state: Position2DDiscreteTheta) -> Position2DDiscreteTheta:
        return Position2DDiscreteTheta(state.x - 1, state.y, state.theta)


class MoveRight(LinearMove):
    def apply(self, state: Position2DDiscreteTheta) -> Position2DDiscreteTheta:
        return Position2DDiscreteTheta(state.x + 1, state.y, state.theta)
