#pragma once

#include "robot_state.hpp"
#include "utils/geometry.hpp"
#include "utils/logger.hpp"
#include <string>
#include <unordered_map>
#include <vector>

struct Map2DConfig {
  double height;
  double width;
  std::vector<Polygon> obstacles;
};

inline const std::unordered_map<std::string, Map2DConfig> mapList{
    {"map_5x10_open",
     Map2DConfig{
         10,
         5,
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
  explicit Map2D(const std::string &mapName,
                 std::shared_ptr<LoggerInterface> logger)
      : config_(mapList.at(mapName)), logger(logger) {
    const Point2D topLeft{0.0, config_.height};
    const Point2D topRight{config_.width, config_.height};
    const Point2D bottomLeft{0.0, 0.0};
    const Point2D bottomRight{config_.width, 0.0};
    this->mapBounds = Polygon({topLeft, topRight, bottomRight, bottomLeft});
    logger->log("Map bounds:");
    for (const auto& point: this->mapBounds.BoostPoly().outer()){
      logger->log(std::to_string(point.x()) + " " + std::to_string(point.y()));
    }
  };

  bool checkStateConsistency(const RobotState &robotState) {
    return !checkOutOfBounds(robotState) && !checkInCollision(robotState);
  }

  Map2DConfig config() const { return config_; }

private:
  const Map2DConfig config_;
  std::shared_ptr<LoggerInterface> logger;
  Polygon mapBounds;

private:
  bool checkInCollision(const RobotState &robotState) {
    for (const auto &obstacle : this->config_.obstacles) {
      if (robotState.contours.intersects(obstacle) ||
          robotState.contours.within(obstacle) ||
          obstacle.within(robotState.contours)) {
        this->logger->log("In collision");
        return true;
      }
    }
    return false;
  };

  bool checkOutOfBounds(const RobotState &robotState) {
    if (!robotState.contours.within(this->mapBounds)) {
      this->logger->log("Out of bounds");
      return true;
    }
    return false;
  }
};