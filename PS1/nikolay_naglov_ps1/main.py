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
from collision_checkers.convolve2d import CollisionCheckerConvolve2D
from agents.agents import AgentNumpyArray
from actions.linear_movements import MoveUp, MoveDown, MoveLeft, MoveRight
from actions.rotations import RotateCW, RotateCCW


def main():
    data = load_data("datasets/data_ps1.npz")
    rod = data["rod"]
    space = data["environment"]

    start_state = Position2DDiscreteTheta(6, 6, 2)
    goal_state = Position2DDiscreteTheta(55, 55, 0)

    # visualize_agent_configs(rod, "results/task_1", "agent_config")
    # visualize_workspace(space, "results/task_1", "workspace")
    # visualize_agent_in_workspace(
    #     rod,
    #     start_state.to_tuple(),
    #     space,
    #     "results/task_1",
    #     "agent_in_start_cfg",
    # )
    # visualize_agent_in_workspace(
    #     rod,
    #     goal_state.to_tuple(),
    #     space,
    #     "results/task_1",
    #     "agent_in_goal_cfg",
    # )

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

    # for angle in range(collision_checker.cspace.shape[2]):
    #     visualize_workspace(
    #         collision_checker.cspace[:, :, angle],
    #         "results/task_1",
    #         f"configuration_space{angle}",
    #     )

    # path_planner = Dijkstra(collision_checker)
    # path_planner = AStarL1Heuristic(collision_checker)
    path_planner = AStarL1WithAngleHeuristic(collision_checker)
    path_planner.start_state = start_state
    path_planner.goal_state = goal_state
    path_planner.workspace = workspace
    path_planner.available_actions = available_actions
    result_path = path_planner.plan().to_list_of_tuples()

    # plot_results(
    #     workspace.space, agent.config, result_path, "results/task_2/dijkstra.mp4"
    # )
    # plot_results(
    #     workspace.space,
    #     agent.config,
    #     result_path,
    #     "results/task_2/a_star_l1_heuristic.mp4",
    # )
    plot_results(
        workspace.space,
        agent.config,
        result_path,
        "results/task_2/a_star_l1_with_angle_heuristic.mp4",
    )

    return 0


if __name__ == "__main__":
    main()
