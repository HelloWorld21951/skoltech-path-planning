#include "planners_server.hpp"
#include "robot_state.hpp"
#include "utils/geometry.hpp"
#include "utils/ros_parameters.hpp"
#include <memory>

PlannersServer::PlannersServer(rclcpp::Node::SharedPtr node)
    : node(node), robotSize(getParameter<double>(node, "robot.length"),
                            getParameter<double>(node, "robot.width")),
      environmentMap(
          std::make_shared<Map2D>(getParameter<std::string>(node, "map_name"))),
      start(getParameter<double>(node, "start.x"),
            getParameter<double>(node, "start.y"),
            degToRad(getParameter<double>(node, "start.theta"))),
      goal(getParameter<double>(node, "goal.x"),
           getParameter<double>(node, "goal.y"),
           degToRad(getParameter<double>(node, "goal.theta"))) {}