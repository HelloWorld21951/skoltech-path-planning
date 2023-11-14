# from planners.a_star import AStarL1Heuristic, AStarL1WithAngleHeuristic, Dijkstra
from states.states import Position2DDiscreteTheta

from utils.data_loader import load_data
from utils.visualizer import (
    plot_results,
    visualize_agent_configs,
    visualize_agent_in_workspace,
    visualize_workspace,
)


def main():
    data = load_data("datasets/data_ps1.npz")
    agent = data["rod"]
    workspace = data["environment"]

    start_state = Position2DDiscreteTheta(6, 6, 2)
    goal_state = Position2DDiscreteTheta(55, 55, 0)

    visualize_agent_configs(agent, "results/task_1", "agent_config")
    visualize_workspace(workspace, "results/task_1", "workspace")
    visualize_agent_in_workspace(
        agent,
        start_state.to_tuple(),
        workspace,
        "results/task_1",
        "agent_in_start_cfg",
    )
    visualize_agent_in_workspace(
        agent,
        goal_state.to_tuple(),
        workspace,
        "results/task_1",
        "agent_in_goal_cfg",
    )
    return 0


if __name__ == "__main__":
    main()
