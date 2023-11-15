import numpy as np
import matplotlib.pyplot as plt
 
def main():
    data = np.load("data_ps1.npz")
    environment = data["environment"]
    rod = data["rod"]

    for i in range(0, rod.shape[2]):
        plt.imsave(
            f"images/rod_config_{i}.png", rod[:, :, i]
        )

    plt.imsave(f"images/environment.png", environment)

if __name__ == "__main__":
    main()