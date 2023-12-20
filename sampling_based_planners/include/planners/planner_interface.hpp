#pragma once

#include "environment/map_2d.hpp"
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

  virtual PlanningResult plan() = 0;

protected:
  Position2D start;
  Position2D goal;
  std::shared_ptr<Map2D> map;
};