import numpy as np
import pickle
from angle_util import angle_difference
from environment import State, ManipulatorEnv
from rrt import RRTPlanner
from video_util import animate_plan


# You are free to change any interfaces for your needs.


def main():
    with open("data.pickle", "rb") as handle:
        data = pickle.load(handle)

    start_state = State(np.array(data["start_state"]))
    goal_state = State(np.array(data["goal_state"]))

    env = ManipulatorEnv(
        obstacles=np.array(data["obstacles"]),
        initial_state=start_state,
        collision_threshold=data["collision_threshold"],
    )

    # Task 1A

    # env.render(plt_imsave=True, save_path="images/start_state.png")

    # env.state = goal_state
    # env.render(plt_imsave=True, save_path="images/goal_state.png")

    # Task 1B

    # random_state_1 = State(np.array([90, 0, 90, 0]))
    # env.state = random_state_1
    # print(
    #     f"Random state: [{random_state_1.angles}]\tCollision: {env.check_collision(random_state_1)}"
    # )
    # env.render(plt_imsave=True, save_path="images/random_state_1.png")

    # random_state_2 = State(np.array([0, 90, -45, -45]))
    # env.state = random_state_2
    # print(
    #     f"Random state: [{random_state_2.angles}]\tCollision: {env.check_collision(random_state_2)}"
    # )
    # env.render(plt_imsave=True, save_path="images/random_state_2.png")

    # random_state_3 = State(np.array([-135, -135, 90, 0]))
    # env.state = random_state_3
    # print(
    #     f"Random state: [{random_state_3.angles}]\tCollision: {env.check_collision(random_state_3)}"
    # )
    # env.render(plt_imsave=True, save_path="images/random_state_3.png")

    # random_state_4 = State(np.array([-90, 90, 0, 0]))
    # env.state = random_state_4
    # print(
    #     f"Random state: [{random_state_4.angles}]\tCollision: {env.check_collision(random_state_4)}"
    # )
    # env.render(plt_imsave=True, save_path="images/random_state_4.png")

    # Task 2A

    env.state = start_state

    def distance(state_1, state_2):
        return np.sum(angle_difference(state_2, state_1))

    planner = RRTPlanner(env, distance)

    print(planner.sample())

    # plan = planner.plan(start_state, goal_state)
    # print("RRT planner has finished successfully")

    # animate_plan(env, plan)


if __name__ == "__main__":
    main()
