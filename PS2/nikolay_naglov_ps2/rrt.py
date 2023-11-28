from typing import List, Callable

import numpy as np

from environment import State, ManipulatorEnv
from angle_util import angle_difference, wrap_angle

class Node:
    def __init__(self, state, parent = None) -> None:
        self.state = state
        self.parent = parent


class RRTPlanner:
    def __init__(
            self, 
            env: ManipulatorEnv, 
            distance_fn: Callable[[State, State], int], 
            max_angle_step: float = 10.0, 
            max_iterations: int = 5000
        ) -> None:
        self._env = env
        self._distance_fn = distance_fn
        self._max_angle_step = max_angle_step
        self._N = 6000
        self._node_list = []
        self._goal_state_probability = 0.1

    def _get_path(self) -> List[State]:
        path = []
        node = self._node_list[-1]
        while node is not None:
            path.append(node.state)
            node = node.parent
        path.reverse()
        print(f"Path length: {len(path)}")
        return path

    def _sample(self, goal_state: State) -> Node:
        if np.random.uniform() < self._goal_state_probability:
            return Node(goal_state)
        angles = np.array(
            [
                np.random.choice(
                    np.arange(-180, 180, 10),
                )
                for i in range(4)
            ]
        )
        return Node(State(angles))
    
    def _find_nearest_node(self, node: Node) -> Node:
        distances = np.array(
        [
                self._distance_fn(node.state, visited_node.state) 
                for visited_node in self._node_list
            ]
        )
        min_id = np.argmin(distances)
        return self._node_list[min_id]

    def _steer(self, node_1: Node, node_2: Node, goal_state: State) -> List[Node]:
        if np.all(node_1.state.angles == node_2.state.angles):
            return []
        result = [node_1]
        delta = angle_difference(node_2.state.angles, node_1.state.angles)
        i = 0
        while i < delta.shape[0]:
            if np.abs(delta[i]) < self._max_angle_step / 2:
                i += 1
                continue
            new_angles = np.copy(result[-1].state.angles)
            new_angles[i] = wrap_angle(
                new_angles[i] + np.sign(delta[i]) * self._max_angle_step
            )
            new_node = Node(State(new_angles), result[-1])
            if self._env.check_collision(new_node.state):
                i += 1
                continue
            else:
                i = 0
            delta = angle_difference(node_2.state.angles, new_angles)
            result.append(new_node)
            delta_goal = angle_difference(goal_state.angles, new_angles)
            if np.all(delta_goal < self._max_angle_step // 2):
                result.pop(0)
                return result
            if np.all(np.abs(delta) < self._max_angle_step // 2):
                result.pop(0)
                return result
        result.pop(0)
        return result

    def plan(self, start_state: State, goal_state: State) -> List[State]:
        self._node_list.append(Node(start_state))
        for i in range(self._N):    
            q_rand = self._sample(goal_state)
            q_near = self._find_nearest_node(q_rand)
            q_new = self._steer(q_near, q_rand, goal_state)
            if len(q_new) == 0:
                continue
            self._node_list.extend(q_new)
            delta = np.abs(
                angle_difference(q_new[-1].state.angles, goal_state.angles)
            )
            if np.all(delta < self._max_angle_step // 2):
                print("Path found")
                print(f"States visited: {len(self._node_list)}")
                return self._get_path()
        print("Path not found")
        return ()
