import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d

from utils import *
from a_star import AStar
 

def main():
    data = np.load("data_ps1.npz")
    environment = data["environment"]
    rod = data["rod"]

    # Task 1A

    for i in range(0, rod.shape[2]):
        plt.imsave(f"images/rod_config_{i}.png", rod[:, :, i])

    plt.imsave(f"images/environment.png", environment)

    # Task 1B

    state = (10, 10, 3)
    rod_in_environment = plot_enviroment(environment, rod, state)
    plt.imsave(f"images/rod_in_environment.png", rod_in_environment)

    # Task 1C

    cspace = np.empty(
        (environment.shape[0], environment.shape[1], rod.shape[2])
    )
    for i in range(rod.shape[2]):
        cspace[:, :, i] = normalize_image(
            convolve2d(environment, rod[:, :, i], "same", "symm")
        )
        plt.imsave(f"images/cspace_{i}.png", cspace[:, :, i])

    # Task 2A

    def collision_function(state):
        collision_on_obstacle = cspace[state[0], state[1], state[2]] == 1
        collision_on_border = (
            state[0] <= rod.shape[0] / 2 
            or state[0] >= environment.shape[0] - rod.shape[0] / 2
            or state[1] <= rod.shape[1] / 2 
            or state[1] >= environment.shape[1] - rod.shape[1] / 2
        )
        return collision_on_obstacle or collision_on_border


    def zero_heuristic(state_1, state_2):
        return 0

    start = (6, 6, 2)
    goal = (55, 55, 0)

    print("Dijkstra:")
    planner = AStar(collision_function, zero_heuristic)
    planner.setup(start, goal)
    path = planner.build_path()

    plotting_results(environment, rod, path)

    # Task 2B

    def l1_heuristic(state_1, state_2):
        return abs(state_2[0] - state_1[0]) + abs(state_2[1] - state_1[1])
    
    print("A* with L1 heuristic")
    planner = AStar(collision_function, l1_heuristic)
    planner.setup(start, goal)
    planner.build_path()

    # Task 2C

    def l1_angle_heuristic(state_1, state_2):
        delta_theta = abs(state_2[2] - state_1[2])
        if delta_theta == 3:
            delta_theta = 1
        return abs(state_2[0] - state_1[0]) + abs(state_2[1] - state_1[1]) + delta_theta
    
    print("A* with L1 and angle heuristic")
    planner = AStar(collision_function, l1_angle_heuristic)
    planner.setup(start, goal)
    planner.build_path()
    
if __name__ == "__main__":
    main()