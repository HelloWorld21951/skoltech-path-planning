import numpy as np
from utils import (
    action_space,
    transition_function,
    probabilistic_transition_function,
    state_consistency_check,
)


def mdp(env, goal, gamma=0.99, max_num_of_iterations=100):
    """
    env is the grid enviroment
    goal is the goal state
    gamma: convergence hyperparamter

    output:
    V: Optimal value function
    """
    V = np.zeros(env.shape)
    V[goal] = 1
    for i in range(max_num_of_iterations):
        new_V = V.copy()
        for row in range(V.shape[0]):
            for column in range(V.shape[1]):
                current_state = (row, column)
                new_value = -np.inf
                for action in action_space:
                    (
                        transition_states,
                        transition_probs,
                    ) = probabilistic_transition_function(env, current_state, action)
                    rewards = []
                    transition_state_value = V[
                        transition_function(env, current_state, action)[0]
                    ]
                    for state in transition_states:
                        if state == goal:
                            rewards.append(1)
                        elif not state_consistency_check(env, state):
                            rewards.append(-1)
                        else:
                            rewards.append(0)
                    current_reward_expectation = np.sum(
                        np.array(transition_probs) * np.array(rewards)
                    )
                    new_value = max(
                        new_value,
                        current_reward_expectation + gamma * transition_state_value,
                    )
                    new_V[current_state] = new_value

        if np.allclose(V, new_V, atol=1e-3):
            print(f"Converged after {i + 1} iterations")
            break

        V = new_V
    V[goal] = np.max(V) + 0.1
    return V


def policy_mdp(env, V):
    """
    env is the grid enviroment
    V: optimal value function

    output:
    policy: a map from each state x to the greedy best action a to execute
    """
    policy = {}
    for row in range(V.shape[0]):
        for column in range(V.shape[1]):
            current_state = (row, column)
            transition_state_values = np.array(
                [
                    V[transition_function(env, current_state, action)[0]]
                    for action in action_space
                ]
            )
            best_action_id = np.argmax(transition_state_values)
            policy[current_state] = action_space[best_action_id]
    return policy
