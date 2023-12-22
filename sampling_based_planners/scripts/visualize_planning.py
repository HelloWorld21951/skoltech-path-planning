import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.transforms import Affine2D


def plot_robot_in_position(ax, position, robot_size, color="blue"):
    ax.add_patch(
        Rectangle(
            (position[0] - robot_size[0] / 2, position[1] - robot_size[1] / 2),
            robot_size[0],
            robot_size[1],
            transform=Affine2D().rotate_deg_around(
                position[0], position[1], position[2]
            )
            + ax.transData,
            facecolor=color,
            fill=True,
        )
    )


def main():
    fig, ax = plt.subplots(figsize=(15, 15))
    map_size = (5.0, 10.0)
    ax.set_xlim(0.0, map_size[0])
    ax.set_ylim(0.0, map_size[1])
    # map border
    ax.add_patch(Rectangle((0.0, 0.0), map_size[0], map_size[1], fill=False))
    # map obstacles
    ax.add_patch(Rectangle((1.0, 1.0), 3.0, 4.0, facecolor="black", fill=True))
    ax.add_patch(Rectangle((1.0, 6.0), 2.0, 4.0, facecolor="black", fill=True))
    ax.add_patch(Rectangle((3.5, 5.5), 4.0, 3.0, facecolor="black", fill=True))
    ax.add_patch(Rectangle((2.0, 5.0), 0.2, 1.0, facecolor="black", fill=True))
    # robot
    robot_size = (0.2, 0.3)
    start = (0.5, 0.5, 0.0)
    goal = (4.5, 9.5, 90.0)
    plot_robot_in_position(ax, start, robot_size, color="red")
    plot_robot_in_position(ax, goal, robot_size, color="green")
    plt.show()


if __name__ == "__main__":
    main()
