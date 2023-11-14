from queue import PriorityQueue
from typing import Dict

from collision_checkers.collision_checker_interface import CollisionChecker
from states.states import State, Position2DDiscreteTheta
from planners.path import Path
from planners.planner_interface import PathPlanner


class AStar(PathPlanner):
    def __init__(self, collision_checker: CollisionChecker) -> None:
        super().__init__(collision_checker)
        self._visited: Dict[State, int] = {}
        self._parent_table: Dict[State, State] = {}
        self._queue = PriorityQueue()

    def _heuristic(self, state_1: State, state_2: State) -> int:
        raise NotImplementedError(
            f"Heuristic function for {self.__class__} is not implemented"
        )

    def _cleanup(self):
        self._visited.clear()
        self._parent_table.clear()
        self._queue = PriorityQueue()
        self.path.clear()

    def _make_path_from_parent_table(self) -> Path:
        list_states = [self.goal_state]
        current_state = self.goal_state
        while current_state != self.start_state:
            current_state = self._parent_table[current_state]
            list_states.append(current_state)
        list_states.reverse()
        cost = self._visited[self.goal_state]
        return Path(list_states, cost)

    def plan(self) -> Path:
        if self.start_state is None:
            raise ValueError(
                f"{self.__class__}: Start state was not set, use set_start_state(state) method before calling plan()"
            )

        if self.goal_state is None:
            raise ValueError(
                f"{self.__class__}: Goal state was not set, use set_goal_state(state) method before calling plan()"
            )

        if self.workspace is None:
            raise ValueError(
                f"{self.__class__}: Workspace was not set, use set_workspace(space) method before calling plan()"
            )

        if self.available_actions is None:
            raise ValueError(
                f"{self.__class__}: List of available actions was not set, use set_available_actions(actions) method before calling plan()"
            )

        self._cleanup()
        self._queue.put((0, self.start_state))
        self._visited[self.start_state] = 0

        while not self._queue.empty():
            current_state = self._queue.get()
            if current_state == self.goal_state:
                return self._make_path_from_parent_table()
            for action in self.available_actions:
                next_state = action.apply(current_state)
                if self._collision_checker.is_collision(next_state):
                    continue
                if next_state not in self._visited.keys():
                    self._visited[next_state] = (
                        self._visited[current_state] + action.cost()
                    )
                    self._parent_table[next_state] = current_state
                    self._queue.put(
                        (
                            self._visited[next_state]
                            + self._heuristic(next_state, self.goal_state)
                        )
                    )
                elif (
                    self._visited[current_state] + action.cost()
                    < self._visited[next_state]
                ):
                    self._visited[next_state] = (
                        self._visited[current_state] + action.cost()
                    )
                    self._parent_table[next_state] = current_state

        print(f"{self.__class__}: Could not find path between states")
        return Path([], 0)


class Dijkstra(AStar[Position2DDiscreteTheta]):
    def __init__(self, collision_checker: CollisionChecker) -> None:
        super().__init__(collision_checker)

    def _heuristic(
        self, state_1: Position2DDiscreteTheta, state_2: Position2DDiscreteTheta
    ) -> int:
        return 0


class AStarL1Heuristic(AStar[Position2DDiscreteTheta]):
    def __init__(self, collision_checker: CollisionChecker) -> None:
        super().__init__(collision_checker)

    def _heuristic(
        self, state_1: Position2DDiscreteTheta, state_2: Position2DDiscreteTheta
    ) -> int:
        return abs(state_2.x - state_1.x) + abs(state_2.y - state_1.y)


class AStarL1WithAngleHeuristic(AStar[Position2DDiscreteTheta]):
    def __init__(self, collision_checker: CollisionChecker) -> None:
        super().__init__(collision_checker)

    def _heuristic(
        self, state_1: Position2DDiscreteTheta, state_2: Position2DDiscreteTheta
    ) -> int:
        return (
            abs(state_2.x - state_1.x)
            + abs(state_2.y - state_1.y)
            + abs(state_2.theta - state_1.theta)
        )
