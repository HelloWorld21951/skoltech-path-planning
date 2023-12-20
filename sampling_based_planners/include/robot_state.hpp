#pragma once

#include "utils/geometry.hpp"

struct RobotSize {
  RobotSize(double length, double width) : length(length), width(width){};

  double length;
  double width;
};

struct RobotState {
  RobotState(const RobotSize &size, const Position2D &position)
      : position(position) {
    const double halfWidth = size.width / 2.0;
    const double halfLength = size.length / 2.0;
    Point2D topLeft{halfLength, -halfWidth};
    Point2D topRight{halfLength, halfWidth};
    Point2D bottomLeft{-halfLength, halfWidth};
    Point2D bottomRight{-halfLength, -halfWidth};

    this->contours = Polygon({position * topLeft, position * topRight,
                              position * bottomRight, position * bottomLeft});
  };

  Polygon contours;
  Position2D position;
};