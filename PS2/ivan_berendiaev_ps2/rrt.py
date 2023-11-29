from typing import List, Callable

import numpy as np

from environment import State, ManipulatorEnv
from angle_util import angle_difference, wrap_angle


class Vertex:
    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent


class Graph:
    def __init__(self, start_state, distance_fn):
        self.vertices = [Vertex(start_state)]
        self.distance_fn = distance_fn

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def find_nearest_vertex(self, state):
        distances = np.array([self.distance_fn(state, vertex.state) for vertex in self.vertices])
        return self.vertices[np.argmin(distances)]
    
    def get_path(self):
        path = []
        vertex = self.vertices[-1]
        while vertex is not None:
            # print(vertex)
            path.append(vertex.state)
            vertex = vertex.parent
        print(f"Path size: {len(path)}")
        return path[::-1]



class RRTPlanner:
    def __init__(self, env: ManipulatorEnv, distance_fn: Callable, max_angle_step: float = 10.0, max_iterations: int = 10000):
        self._env = env
        self._distance_fn = distance_fn
        self._max_angle_step = max_angle_step
        self.max_iterations = max_iterations

    def sample(self, goal_state: State):
        if np.random.uniform() < 0.1:
            return goal_state
        angles = np.array(
            [
                np.random.choice(
                    np.arange(-180, 180, 10),
                )
                for i in range(4)
            ]
        )
        return State(angles)

    def steer(self, from_: Vertex, to_: State, goal_state: State):
        if np.array_equal(from_.state.angles, to_.angles):
            return []
        result = [from_]
        delta_to = angle_difference(to_.angles, from_.state.angles)
        i = 0
        while i < 4:
            if np.abs(delta_to[i]) < self._max_angle_step / 2:
                i += 1
                continue
            next_angles = np.copy(result[-1].state.angles)
            next_angles[i] = wrap_angle(
                next_angles[i] + np.sign(delta_to[i]) * self._max_angle_step
            )
            next_state = State(next_angles)
            if self._env.check_collision(next_state):
                i += 1
                continue
            else:
                i = 0
                result.append(Vertex(next_state, result[-1]))
            delta_to = angle_difference(to_.angles, next_angles)
            delta_goal = angle_difference(goal_state.angles, next_angles)
            if np.all(delta_goal < self._max_angle_step / 2) or np.all(np.abs(delta_to) < self._max_angle_step / 2):
                return result
        return result

    def plan(self, start_state: State, goal_state: State) -> List[State]:
        self.graph = Graph(start_state, self._distance_fn)
        for i in range(self.max_iterations):    
            rnd = self.sample(goal_state)
            near = self.graph.find_nearest_vertex(rnd)
            new = self.steer(near, rnd, goal_state)
            if len(new) == 0:
                continue
            for i in range(1, len(new)):
                self.graph.add_vertex(new[i])
            delta = np.abs(angle_difference(new[-1].state.angles, goal_state.angles))
            if np.all(delta < self._max_angle_step / 2):
                print("Planning succeeded")
                print(f"Visited total of {len(self.graph.vertices)} states")
                return self.graph.get_path()
        print("Planning failed")
        return ()
