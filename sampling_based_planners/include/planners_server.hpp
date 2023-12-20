#pragma once

#include "environment/map_2d.hpp"
#include "planners/planner_interface.hpp"
#include "robot_state.hpp"
#include "utils/geometry.hpp"
#include "utils/logger.hpp"
#include <memory>
#include <rclcpp/node.hpp>
#include <rclcpp/publisher.hpp>

class PlannersServer {
public:
  PlannersServer(rclcpp::Node::SharedPtr node);

private:
  rclcpp::Node::SharedPtr node;
  std::shared_ptr<LoggerInterface> logger;
  std::shared_ptr<PlannerInterface> planner;
  const RobotSize robotSize;
  std::shared_ptr<Map2D> environmentMap;
  const Position2D start;
  const Position2D goal;
};