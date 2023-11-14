import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os

from utils.image_utils import merge_enviroment


def visualize_agent_configs(configs: np.ndarray, folder: str, filename: str):
    for cfg_num in range(0, configs.shape[2]):
        plt.figure(figsize=(100, 100))
        plt.imsave(
            os.path.join(folder, f"{filename}{cfg_num}.png"), configs[:, :, cfg_num]
        )


def visualize_workspace(workspace: np.ndarray, folder: str, filename: str):
    plt.imsave(os.path.join(folder, f"{filename}.png"), workspace)


def visualize_agent_in_workspace(
    agent: np.ndarray, state: tuple, workspace: np.ndarray, folder: str, filename: str
):
    image = merge_enviroment(workspace, agent, state)
    plt.imsave(os.path.join(folder, f"{filename}.png"), image)


def plot_results(
    environment: np.ndarray,
    rod: np.ndarray,
    plan: list,
    save_path: str = "rod_solve.mp4",
):
    """
    create an animation of the plan and save it to a file

    @param environment: the environment image in 2d
    @param rod: is the 3d array of different configuration
    @param plan: list of poses
    @param save_path: path to save the animation
    """

    fig = plt.figure()
    imgs = []

    for s in plan:
        im = merge_enviroment(environment, rod, s)
        plot = plt.imshow(im)
        imgs.append([plot])

    ani = animation.ArtistAnimation(fig, imgs, interval=50, blit=True)

    ani.save(save_path)

    plt.show()
