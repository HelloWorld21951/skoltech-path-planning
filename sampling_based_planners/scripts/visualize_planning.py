import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.transforms import Affine2D


def plot_robot_in_position(ax, position, robot_size, color="blue", fill=False):
    ax.add_patch(
        Rectangle(
            (position[0] - robot_size[0] / 2, position[1] - robot_size[1] / 2),
            robot_size[0],
            robot_size[1],
            angle=position[2],
            rotation_point=(position[0], position[1]),
            facecolor=color,
            edgecolor=color,
            fill=fill,
        )
    )


def main():
    fig, ax = plt.subplots(figsize=(10, 10))
    map_size = (5.0, 10.0)
    ax.set_xlim(0.0, map_size[0])
    ax.set_ylim(0.0, map_size[1])
    ax.axes.set_aspect("equal")
    images_folder = "images"

    # map border

    ax.add_patch(Rectangle((0.0, 0.0), map_size[0], map_size[1], fill=False))

    # map obstacles

    ax.add_patch(Rectangle((1.0, 1.0), 3.0, 4.0, facecolor="black", fill=True))
    ax.add_patch(Rectangle((1.0, 6.0), 2.0, 4.0, facecolor="black", fill=True))
    ax.add_patch(Rectangle((4.0, 6.0), 4.0, 3.0, facecolor="black", fill=True))
    ax.add_patch(Rectangle((2.0, 5.0), 0.2, 1.0, facecolor="black", fill=True))

    # robot

    robot_size = (0.4, 0.8)
    start = (0.5, 0.5, 0.0)
    goal = (4.5, 9.5, 90.0)
    plot_robot_in_position(ax, start, robot_size, color="red", fill=True)
    plot_robot_in_position(ax, goal, robot_size, color="lime", fill=True)
    plt.savefig(f"{images_folder}/small_map.png")

    # RRTStar
    path = [
        start,
        (2.5, 0.52, 5.0),
        (4.33, 0.57, 12.0),
        (4.5, 3.1, 23.0),
        (4.35, 5.2, 43.0),
        (3.54, 5.85, 59.0),
        (3.5, 9.0, 77.0),
        (3.67, 9.45, 90.0),
        goal,
    ]

    # path states

    for position in path:
        plot_robot_in_position(ax, position, robot_size)

    x = [pos[0] for pos in path]
    y = [pos[1] for pos in path]
    ax.plot(x, y, marker=".")
    plt.savefig(f"{images_folder}/rrt_star_small_map.png")

    plt.show()


if __name__ == "__main__":
    main()
