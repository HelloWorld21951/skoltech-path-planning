#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from utils import plot_enviroment, action_space, record_plan, transition_function
from vi import vi, policy_vi
from mdp import mdp, policy_mdp


data = np.load("data_ps3.npz")
environment = data["environment"]

# (row index, colum index). In the image row corresponds to y, and colum to x.
x_ini = (11, 6)
goal = (15, 29)


# task 1 VI, Gopt
# ======================================
task_1_folder = "results/task_1"
Gopt = vi(environment, goal)
plt.imshow(Gopt)
plt.savefig(f"{task_1_folder}/final_G.png")
plt.clf()

iterations = [1]
iterations.extend(list(range(10, 70, 10)))

for i in iterations:
    G = vi(environment, goal, max_num_of_iterations=i)
    plt.imshow(G)
    plt.savefig(f"{task_1_folder}/G_{i}_iters.png")
    plt.clf()


# task 2: Plan
# ======================================
task_2_folder = "results/task_2"
policy = policy_vi(environment, Gopt)


def vi_plan_iteration(x):
    return transition_function(environment, x, policy[x])[0]


record_plan(
    environment,
    x_ini,
    goal,
    vi_plan_iteration,
    f"{task_2_folder}/plan_vi.mp4",
)


# task 3 MDP, Vopt
# ======================================
# Vopt = mdp(environment,goal)

# Visualization
# ======================================
