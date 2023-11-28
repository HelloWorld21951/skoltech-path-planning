import numpy as np
import pickle
from angle_util import angle_difference
from environment import State, ManipulatorEnv
from rrt import RRTPlanner
from video_util import animate_plan


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

    folder_task_1 = "results/task_1"
    folder_task_2 = "results/task_2"

    # 1A

    env.render(plt_imsave=True, save_path=f"{folder_task_1}/start_state.png")
    env.state = goal_state
    env.render(plt_imsave=True, save_path=f"{folder_task_1}/goal_state.png")

    # 1B

    random_state_1 = State(np.array([90, 0, 90, 0]))
    env.state = random_state_1
    print(
        f"Random state: [{random_state_1.angles}]\tCollision: {env.check_collision(random_state_1)}"
    )
    env.render(plt_imsave=True, save_path=f"{folder_task_1}/random_state_1.png")

    random_state_2 = State(np.array([0, 90, -45, -45]))
    env.state = random_state_2
    print(
        f"Random state: [{random_state_2.angles}]\tCollision: {env.check_collision(random_state_2)}"
    )
    env.render(plt_imsave=True, save_path=f"{folder_task_1}/random_state_2.png")

    random_state_3 = State(np.array([-135, -135, 90, 0]))
    env.state = random_state_3
    print(
        f"Random state: [{random_state_3.angles}]\tCollision: {env.check_collision(random_state_3)}"
    )
    env.render(plt_imsave=True, save_path=f"{folder_task_1}/random_state_3.png")

    random_state_4 = State(np.array([-90, 90, 0, 0]))
    env.state = random_state_4
    print(
        f"Random state: [{random_state_4.angles}]\tCollision: {env.check_collision(random_state_4)}"
    )
    env.render(plt_imsave=True, save_path=f"{folder_task_1}/random_state_4.png")

    # 2A

    print("\n---Classic RRT---\n")

    env.state = start_state

    def distance(state_1, state_2):
        return np.sum(np.abs(angle_difference(state_2.angles, state_1.angles)))

    planner = RRTPlanner(env, distance)
    plan = planner.plan(start_state, goal_state)
    animate_plan(env, plan, f"{folder_task_2}/plan_rrt.mp4")

    # 2C


    print("\n---RRT with weighted distance---\n")

    env.state = start_state

    def distance_angles_weighted(state_1, state_2):
        distance = 0
        number_of_angles = state_1.angles.shape[0]
        for i in range(number_of_angles):
            distance += np.abs(angle_difference(state_2.angles[i], state_1.angles[i])) * (number_of_angles - 1)
        return distance

    planner = RRTPlanner(env, distance_angles_weighted)
    plan = planner.plan(start_state, goal_state)
    animate_plan(env, plan, f"{folder_task_2}/plan_weighted.mp4")

    # 2D
    
    print("\n---RRT with increased step size---\n")

    env.state = start_state

    def distance(state_1, state_2):
        return np.sum(np.abs(angle_difference(state_2.angles, state_1.angles)))

    planner = RRTPlanner(env, distance, 15)
    plan = planner.plan(start_state, goal_state)
    animate_plan(env, plan, f"{folder_task_2}/plan_big_step.mp4")


if __name__ == "__main__":
    main()
