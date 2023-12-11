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
                    transition_states_values = []
                    for state in transition_states:
                        if not state_consistency_check(env, state):
                            rewards.append(-1)
                            transition_states_values.append(0)
                        elif state == goal:
                            rewards.append(1)
                            transition_states_values.append(V[state])
                        else:
                            rewards.append(0)
                            transition_states_values.append(V[state])
                    current_reward_expectation = np.sum(
                        np.array(transition_probs) * np.array(rewards)
                    )
                    transition_value_expectation = np.sum(
                        np.array(transition_probs) * np.array(transition_states_values)
                    )
                    new_value = max(
                        new_value,
                        current_reward_expectation
                        + gamma * transition_value_expectation,
                    )
                    new_V[current_state] = new_value

        if np.allclose(V, new_V, atol=1e-3):
            print(f"Converged after {i + 1} iterations")
            break

        V = new_V
    V[goal] = np.max(V)
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
