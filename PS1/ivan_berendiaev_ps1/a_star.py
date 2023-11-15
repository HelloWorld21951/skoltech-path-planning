import numpy as np
from queue import PriorityQueue

from actions import *

class AStar:
    def __init__(self, collision_function, heuristic_function):
        self.collision_function = collision_function
        self.heuristic_function = heuristic_function
        self.visited_states = []
        self.costs = {}
        self.parent_table = {}
        self.queue = PriorityQueue()


    def setup(self, start, goal):
        self.start = start
        self.goal = goal
        self.visited_states.clear()
        self.costs.clear()
        self.parent_table.clear()
        self.queue = PriorityQueue()

    def parent_table_to_path(self):
        path = [self.goal]
        state = self.goal
        while state != self.start:
            state = self.parent_table[state]
            path.append(state)
        path.reverse()
        return path

    def build_path(self):
        self.queue.put((0, self.start))
        self.visited_states.append(self.start)
        self.costs[self.start] = 0

        while not self.queue.empty():
            state = self.queue.get()[1]
            if state == self.goal:
                path = self.parent_table_to_path()
                print(f"Found a path with cost {self.costs[self.goal]} after visiting {len(self.visited_states)} states")
                return path
            for action in [Up, Down, Left, Right, TurnClockwise, TurnCounterClockwise]:
                next_state = action.apply(state)
                if self.collision_function(next_state):
                    continue
                if next_state not in self.visited_states:
                    self.visited_states.append(next_state)
                    self.costs[next_state] = self.costs[state] + 1
                    self.parent_table[next_state] = state
                    self.queue.put(
                        (
                            self.costs[next_state]
                            + self.heuristic_function(next_state, self.goal),
                            next_state
                        )
                    )
                elif self.costs[state] + 1 < self.costs[next_state]:
                    self.costs[next_state] = self.costs[state] + 1
                    self.parent_table[next_state] = state

        print(f"Path was not found")
        return []