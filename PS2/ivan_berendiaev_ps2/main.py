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

    # Task 1A

    env.render(save_img=True, savefile="images/start_state.png")
    env.state = goal_state
    env.render(save_img=True, savefile="images/goal_state.png")

    # Task 1B

    states = [
        State(np.array([10, 15, 50, 100])),
        State(np.array([-30, 120, 0, 0])),
        State(np.array([90, -20, 30, 40])),
        State(np.array([5, 140, 10, 0])),
    ]

    for i, state in enumerate(states):
        env.state = state
        env.render(save_img=True, savefile=f"images/state{i}.png")
        if env.check_collision(state):
            print("Collision")
        else:
            print("No collision")

    # Task 2A

    def distance(state_1, state_2):
        return np.sum(np.abs(angle_difference(state_2.angles, state_1.angles)))

    env.state = start_state
    planner = RRTPlanner(env, distance)
    plan = planner.plan(start_state, goal_state)
    animate_plan(env, plan)

    # Task 2C

    def distance_weighted_sum_of_angles(state_1, state_2):
        distance = 0
        deltas = np.abs(angle_difference(state_2.angles, state_1.angles))
        for i in range(4):
            distance += deltas[i] * (4 - i)
        return distance

    env.state = start_state
    planner = RRTPlanner(env, distance_weighted_sum_of_angles)
    plan = planner.plan(start_state, goal_state)
    print(len(plan))
    animate_plan(env, plan, None)

    # Task 2D
    
    def distance(state_1, state_2):
        return np.sum(np.abs(angle_difference(state_2.angles, state_1.angles)))

    env.state = start_state
    planner = RRTPlanner(env, distance, 8)
    plan = planner.plan(start_state, goal_state)
    print(len(plan))
    animate_plan(env, plan, None)


if __name__ == "__main__":
    main()
