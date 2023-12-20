from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_path(package: str, folder: str, filename: str) -> str:
    return (
        f"{get_package_share_directory('sampling_based_planners')}/{folder}/{filename}"
    )


def generate_launch_description() -> LaunchDescription:
    print(
        get_package_share_directory("sampling_based_planners")
        + "/config/planner_config.yaml"
    )
    return LaunchDescription(
        [
            Node(
                package="sampling_based_planners",
                executable="planners_node",
                parameters=[
                    generate_path(
                        get_package_share_directory("sampling_based_planners"),
                        "config",
                        "planner_config.yaml",
                    )
                ],
                output="screen",
            )
        ]
    )
