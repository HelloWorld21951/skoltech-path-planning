#pragma once

#include "environment/map_2d.hpp"
#include "robot_state.hpp"
#include "utils/geometry.hpp"
#include <memory>

enum class PlanningResult {
  SUCCESS = 1,
  BAD_START = 2,
  BAD_GOAL = 3,
  PATH_NOT_FOUND = 4,
};

class PlannerInterface {
public:
  void setMap(std::shared_ptr<Map2D> map) { this->map = map; };
  void setStart(const Position2D &start) { this->start = start; };
  void setGoal(const Position2D &goal) { this->goal = goal; };
  void setRobotSize(const RobotSize &robotSize) { this->robotSize = robotSize; }

  virtual PlanningResult plan() = 0;

  virtual ~PlannerInterface() = default;

protected:
  Position2D start{0.0, 0.0, 0.0};
  Position2D goal{0.0, 0.0, 0.0};
  std::shared_ptr<Map2D> map;
  RobotSize robotSize;
};