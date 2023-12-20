#pragma once

#include "robot_state.hpp"
#include "utils/geometry.hpp"
#include <unordered_map>
#include <vector>

struct Map2DConfig {
  double length;
  double width;
  std::vector<Polygon> obstacles;
};

inline const std::unordered_map<std::string, Map2DConfig> mapList{
    {"map_5x10_open",
     Map2DConfig{
         5,
         10,
         {
             Polygon({{0.2, 0.2}, {0.2, 0.6}, {1.0, 0.6}, {1.0, 0.2}}),
             Polygon({{3.0, 5.5}, {4.0, 6.1}, {4.0, 5.0}}),
         },
     }},
    {"map_5x10_cluttered",
     Map2DConfig{
         5,
         10,
         {},
     }},
    {"map_500x1000_open",
     Map2DConfig{
         500,
         1000,
         {},
     }},
    {"map_500x1000_cluttered",
     Map2DConfig{
         500,
         1000,
         {},
     }},
};

class Map2D {
public:
  explicit Map2D(const std::string &mapName) : config(mapList.at(mapName)) {
    const double halfWidth = config.width / 2.0;
    const double halfLength = config.length / 2.0;
    const Point2D topLeft{halfLength, -halfWidth};
    const Point2D topRight{halfLength, halfWidth};
    const Point2D bottomLeft{-halfLength, halfWidth};
    const Point2D bottomRight{-halfLength, -halfWidth};
    this->mapBounds = Polygon({topLeft, topRight, bottomRight, bottomLeft});
  };

  bool checkStateConsistency(const RobotState &robotState) {
    return checkInBounds(robotState) && checkInCollision(robotState);
  }

private:
  const Map2DConfig config;
  Polygon mapBounds;

private:
  bool checkInCollision(const RobotState &robotState) {
    for (const auto &obstacle : this->config.obstacles) {
      if (robotState.contours.intersects(obstacle) ||
          robotState.contours.within(obstacle) ||
          obstacle.within(robotState.contours)) {
        return true;
      }
    }
    return false;
  };

  bool checkInBounds(const RobotState &robotState) {
    return !robotState.contours.within(this->mapBounds);
  }
};