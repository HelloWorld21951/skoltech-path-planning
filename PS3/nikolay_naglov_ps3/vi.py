import numpy as np
from utils import action_space, transition_function


def vi(env, goal, max_num_of_iterations=100):
    """
    env is the grid enviroment
    goal is the goal state

    output:
    G: Optimal cost-to-go
    """

    G = np.full(env.shape, np.inf)
    G[goal] = 0
    for i in range(max_num_of_iterations):
        new_G = G.copy()
        for row in range(G.shape[0]):
            for column in range(G.shape[1]):
                current_state = (row, column)
                for action in action_space:
                    transition_state, success = transition_function(
                        env, current_state, action
                    )
                    if not success:
                        continue
                    new_G[transition_state] = min(
                        new_G[transition_state], G[current_state] + 1
                    )
        if np.array_equal(G, new_G):
            print(f"Converged after {i} iterations")
            break
        G = new_G
    return G


def policy_vi(env, G):
    """
    env is the grid enviroment
    G: optimal cost-to-go function

    output:
    policy: a map from each state x to the best action a to execcute
    """
    policy = {}
    return policy
