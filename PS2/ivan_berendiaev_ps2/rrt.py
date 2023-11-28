import copy
import dataclasses
from typing import List, Callable, Union

import numpy as np

from environment import State, ManipulatorEnv
from angle_util import angle_difference, wrap_angle

class Node:
    def __init__(self, state, parent = None) -> None:
        self.state = state
        self.parent = parent


class RRTPlanner:
    def __init__(self, env: ManipulatorEnv, distance_fn: Callable, max_angle_step: float = 10.0) -> None:
        self._env = env
        self._distance_fn = distance_fn
        self._max_angle_step = max_angle_step
        self._N = 6000
        self._node_list = []
        self._goal_state_probability = 0.1

    def sample(self, goal_state: State):
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
    
    def find_nearest_node(self, node: Node):
        distances = np.array([self._distance_fn(node.state, visited_node.state) for visited_node in self._node_list])
        min_id = np.argmin(distances)
        return self._node_list[min_id]

    def get_path(self):
        path = []
        node = self._node_list[-1]
        while node is not None:
            path.append(node.state)
            node = node.parent
        path.reverse()
        return path

    def steer(self, node_1: Node, node_2: Node, goal_state: State):
        if np.all(node_1.state.angles == node_2.state.angles):
            return []
        result = [node_1]
        delta = angle_difference(node_2.state.angles, node_1.state.angles)
        # for i in range(delta.shape[0]):
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
            q_rand = self.sample(goal_state)
            q_near = self.find_nearest_node(q_rand)
            q_new = self.steer(q_near, q_rand, goal_state)
            if len(q_new) == 0:
                continue
            self._node_list.extend(q_new)
            delta = np.abs(angle_difference(q_new[-1].state.angles, goal_state.angles))
            if np.all(delta < self._max_angle_step // 2):
                print("Path found")
                print(len(self._node_list))
                return self.get_path()
        print("Path not found")
        return ()

# class RRTPlanner:
#     def __init__(
#         self, env: ManipulatorEnv, distance_fn: Callable, max_angle_step: float = 10.0
#     ):
#         """
#         :param env: manipulator environment
#         :param distance_fn: function distance_fn(state1, state2) -> float
#         :param max_angle_step: max allowed step for each joint in degrees
#         """
#         self._env = env
#         self._distance_fn = distance_fn
#         self._max_angle_step = max_angle_step
#         self._N = 8000
#         self._vertices = []
#         self._edges = []
#         self._goal_point_probability = 0.2
#         # self._G = {}

#     def sample(self, goal_state: State):
#         if np.random.uniform() < self._goal_point_probability:
#             return goal_state
#         angles = np.array(
#             [
#                 np.random.choice(
#                     np.arange(-180, 180, 10),
#                 )
#                 for i in range(4)
#             ]
#         )
#         return State(angles)

#     def find_nearest(self, state: State):
#         distances = np.array(
#             [
#                 self._distance_fn(visited_state, state)
#                 for visited_state in self._vertices
#             ]
#         )
#         idx = np.argmin(distances)
#         return self._vertices[idx]

#     def steer(self, state_1: State, state_2: State, goal_state: State):
#         result = state_1
#         delta = angle_difference(state_2.angles, state_1.angles)
#         for i in range(delta.shape[0]):
#             if np.abs(delta[i]) < self._max_angle_step / 2:
#                 continue
#             new_angles = np.copy(result.angles)
#             new_angles[i] = wrap_angle(
#                 new_angles[i] + np.sign(delta[i]) * self._max_angle_step
#             )
#             new_state = State(new_angles)
#             if self._env.check_collision(new_state):
#                 continue
#             delta = angle_difference(state_2.angles, new_angles)
#             result = new_state
#             delta_goal = angle_difference(result.angles, goal_state.angles)
#             if np.all(delta_goal < self._max_angle_step / 2):
#                 return result
#             if np.all(np.abs(delta) < self._max_angle_step / 2):
#                 return result
#         return result

#     def plan(self, start_state: State, goal_state: State) -> List[State]:
#         self._vertices.append(start_state)
#         for i in range(self._N):
#             # print(i)
#             q_rand = self.sample(goal_state)
#             q_near = self.find_nearest(q_rand)
#             q_new = self.steer(q_near, q_rand, goal_state)
#             if q_new == q_near:
#                 continue
#             self._vertices.append(q_new)
#             self._edges.append((q_new, q_near))
#             delta = np.abs(angle_difference(q_new.angles, goal_state.angles))
#             if np.count_nonzero(delta < self._max_angle_step / 2) >= 2:
#                 print(q_new.angles)
#             if np.all(delta < self._max_angle_step / 2):
#                 print("Path found")
#                 return ()
#         print("Path not found")
#         return ()

    # def find_nearest(self, state: State):
    #     visited_states = list(self._G.keys())
    #     distances = np.array(
    #         [
    #             self._distance_fn(visited_state, state)
    #             for visited_state in visited_states
    #         ]
    #     )
    #     idx = np.argmin(distances)
    #     return visited_states[idx]

    # def steer(self, state_1: State, state_2: State, goal_state: State):
    #     result = state_1
    #     delta = angle_difference(state_2.angles, state_1.angles)
    #     while not np.all(np.abs(delta) < self._max_angle_step / 2):
    #         i = np.random.choice(4)
    #         if np.abs(delta[i]) < self._max_angle_step / 2:
    #             continue
    #         new_angles = np.copy(result.angles)
    #         new_angles[i] = wrap_angle(
    #             new_angles[i] + np.sign(delta[i]) * self._max_angle_step
    #         )
    #         new_state = State(new_angles)
    #         if self._env.check_collision(new_state):
    #             return result
    #         result = new_state
    #         delta_goal = angle_difference(result.angles, goal_state.angles)
    #         if np.all(delta_goal < self._max_angle_step / 2):
    #             return result
    #     return result

    # def plan(self, start_state: State, goal_state: State) -> List[State]:
    #     self._G[start_state] = None
    #     for i in range(self._N):
    #         # print(i)
    #         q_rand = self.sample()
    #         q_near = self.find_nearest(q_rand)
    #         q_new = self.steer(q_near, q_rand, goal_state)
    #         self._G[q_new] = q_near
    #         delta = np.abs(angle_difference(q_new.angles, goal_state.angles))
    #         if np.count_nonzero(delta < self._max_angle_step / 2) >= 2:
    #             print(q_new.angles)
    #         if np.all(delta < self._max_angle_step / 2):
    #             print("Path found")
    #             return ()
    #     print("Path not found")
    #     return ()
