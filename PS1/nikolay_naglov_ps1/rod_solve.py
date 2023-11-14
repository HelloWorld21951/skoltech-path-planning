from argparse import ArgumentParser, ArgumentError

from actions.linear_movements import MoveUp, MoveDown, MoveLeft, MoveRight
from actions.rotations import RotateCW, RotateCCW
from agents.agents import AgentNumpyArray
from collision_checkers.convolve2d import CollisionCheckerConvolve2D
from planners.a_star import AStarL1Heuristic, AStarL1WithAngleHeuristic, Dijkstra
from states.states import Position2DDiscreteTheta
from spaces.spaces import WorkspaceNumpyArray
from utils.data_loader import load_data
from utils.visualizer import (
    plot_results,
    visualize_agent_configs,
    visualize_agent_in_workspace,
    visualize_workspace,
)


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument("--planner-type", type=str, required=True, default="dijkstra")
    return parser.parse_args()


def main():
    args = get_arguments()

    data = load_data("datasets/data_ps1.npz")
    rod = data["rod"]
    space = data["environment"]

    start_state = Position2DDiscreteTheta(6, 6, 2)
    goal_state = Position2DDiscreteTheta(55, 55, 0)

    visualize_agent_configs(rod, "results/task_1", "agent_config")
    visualize_workspace(space, "results/task_1", "workspace")
    visualize_agent_in_workspace(
        rod,
        start_state.to_tuple(),
        space,
        "results/task_1",
        "agent_in_start_cfg",
    )
    visualize_agent_in_workspace(
        rod,
        goal_state.to_tuple(),
        space,
        "results/task_1",
        "agent_in_goal_cfg",
    )

    workspace = WorkspaceNumpyArray(space)
    agent = AgentNumpyArray(rod)
    collision_checker = CollisionCheckerConvolve2D(workspace, agent)
    available_actions = [
        MoveUp(),
        MoveDown(),
        MoveLeft(),
        MoveRight(),
        RotateCW(),
        RotateCCW(),
    ]

    for angle in range(collision_checker.cspace.shape[2]):
        visualize_workspace(
            collision_checker.cspace[:, :, angle],
            "results/task_1",
            f"configuration_space{angle}",
        )

    planner_type_to_object = {
        "dijkstra": Dijkstra,
        "a_star_l1": AStarL1Heuristic,
        "a_star_l1_angle": AStarL1WithAngleHeuristic,
    }

    planner_type = args.planner_type

    if planner_type in planner_type_to_object.keys():
        path_planner = planner_type_to_object[planner_type](collision_checker)
    else:
        raise ArgumentError(
            f"Planner name {args.planner_type} does not exist. Use one of the following: {planner_type_to_object.keys()}"
        )

    path_planner.start_state = start_state
    path_planner.goal_state = goal_state
    path_planner.workspace = workspace
    path_planner.available_actions = available_actions
    result_path = path_planner.plan().to_list_of_tuples()

    plot_results(
        workspace.space,
        agent.config,
        result_path,
        f"results/task_2/{planner_type}.mp4",
    )

    return 0


if __name__ == "__main__":
    main()
