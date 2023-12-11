import numpy as np
from utils import (
    action_space,
    transition_function,
    probabilistic_transition_function,
    state_consistency_check,
)


def mdp(env, goal, gamma=0.99):
    """
    env is the grid enviroment
    goal is the goal state
    gamma: convergence hyperparamter

    output:
    G: Optimal cost-to-go
    """
    G = np.empty(env.shape)
    G.fill(0)
    G[goal] = 1
    for _ in range(100):
        G_new = G.copy()
        for i in range(G.shape[0]):
            for j in range(G.shape[1]):
                new_value = -np.inf
                for action in action_space:
                    new_states, probs = probabilistic_transition_function(
                        env, (i, j), action
                    )
                    rewards = []
                    for state in new_states:
                        if not state_consistency_check(env, state):
                            rewards.append(-1)
                        elif state == goal:
                            rewards.append(1)
                        else:
                            rewards.append(0)
                    expected_reward = np.sum(np.array(probs) * np.array(rewards))
                    new_state_value = G[transition_function(env, (i, j), action)[0]]
                    new_value = max(
                        new_value,
                        expected_reward + gamma * new_state_value,
                    )
                    G_new[(i, j)] = new_value
        G = G_new
    G[goal] = np.max(G)
    return G


def policy_mdp(env, V):
    """
    env is the grid enviroment
    V: optimal value function

    output:
    policy: a map from each state x to the greedy best action a to execcute
    """
    policy = {}
    for i in range(30):
        for j in range(30):
            new_states_values = []
            for action in action_space:
                new_states_values.append(V[transition_function(env, (i, j), action)[0]])
            min_value_id = 0
            min_value = new_states_values[0]
            for k, value in enumerate(new_states_values):
                if value < min_value:
                    min_value = value
                    min_value_id = k
            policy[(i, j)] = action_space[min_value_id]
    return policy
