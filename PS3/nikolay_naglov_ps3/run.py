#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from utils import plot_enviroment, action_space, transition_function
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
policy = policy_vi(environment, Gopt)


# task 3 MDP, Vopt
# ======================================
# Vopt = mdp(environment,goal)

# Visualization
# ======================================
if 0:
    fig = plt.figure()
    imgs = []
    x = x_ini
    for plan_iters in range(100):
        im = plot_enviroment(environment, x, goal)
        plot = plt.imshow(im)
        imgs.append([plot])

        # TODO, calculate a plan based on the policy calcualted in VI or MDP

        if x == goal:
            print("Goal achieved in iters =", plan_iters)
            break

    im = plot_enviroment(environment, x, goal)
    plot = plt.imshow(im)
    imgs.append([plot])
    ani = animation.ArtistAnimation(fig, imgs, interval=100, blit=True)
    ani.save("plan_vi.mp4")
    # ani.save('plan_mdp.mp4')
    plt.show()
