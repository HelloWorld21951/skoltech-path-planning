import numpy as np
from utils import action_space, transition_function


def vi(env, goal):
    """
    env is the grid enviroment
    goal is the goal state

    output:
    G: Optimal cost-to-go
    """
    G = np.empty(env.shape)
    G.fill(np.inf)
    G[goal] = 0
    for _ in range(100):
        G_new = G.copy()
        for i in range(30):
            for j in range(30):
                for action in action_space:
                    new_state, can_transition = transition_function(env, (i, j), action)
                    if can_transition:
                        G_new[new_state] = min(G_new[new_state], G[(i, j)] + 1)
        G = G_new
    return G


def policy_vi(env, G):
    """
    env is the grid enviroment
    G: optimal cot-to-go function

    output:
    policy: a map from each state x to the best action a to execcute
    """
    policy = {}
    for i in range(30):
        for j in range(30):
            new_states_values = []
            for action in action_space:
                new_states_values.append(G[transition_function(env, (i, j), action)[0]])
            min_value_id = 0
            min_value = new_states_values[0]
            for k, value in enumerate(new_states_values):
                if value < min_value:
                    min_value = value
                    min_value_id = k
            policy[(i, j)] = action_space[min_value_id]
    return policy
