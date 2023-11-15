import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d

from utils import *
 
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

if __name__ == "__main__":
    main()