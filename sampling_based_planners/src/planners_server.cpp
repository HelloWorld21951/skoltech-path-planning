#include "planners_server.hpp"
#include "environment/map_2d.hpp"
#include "planners/ompl/prm_star.hpp"
#include "planners/planner_interface.hpp"
#include "robot_state.hpp"
#include "utils/geometry.hpp"
#include "utils/logger.hpp"
#include "utils/ros_parameters.hpp"
#include <memory>

PlannersServer::PlannersServer(rclcpp::Node::SharedPtr node)
    : node(node), logger(std::make_shared<RosLogger>(node)),
      planner(std::make_shared<PRMStarOMPLPlanner>(logger)),
      robotSize(RobotSize{getParameter<double>(node, "robot.length"),
                          getParameter<double>(node, "robot.width")}),
      environmentMap(std::make_shared<Map2D>(
          getParameter<std::string>(node, "map_name"), logger)),
      start(getParameter<double>(node, "start.x"),
            getParameter<double>(node, "start.y"),
            degToRad(getParameter<double>(node, "start.theta"))),
      goal(getParameter<double>(node, "goal.x"),
           getParameter<double>(node, "goal.y"),
           degToRad(getParameter<double>(node, "goal.theta"))) {
  planner->setRobotSize(this->robotSize);
  planner->setMap(this->environmentMap);
  planner->setStart(this->start);
  planner->setGoal(this->goal);
  planner->plan();
}