#pragma once

#include <Eigen/Dense>
#include <boost/geometry/algorithms/append.hpp>
#include <boost/geometry/algorithms/detail/intersects/interface.hpp>
#include <boost/geometry/algorithms/detail/within/interface.hpp>
#include <boost/geometry/algorithms/intersects.hpp>
#include <boost/geometry/geometries/point_xy.hpp>
#include <boost/geometry/geometries/polygon.hpp>
#include <cmath>
#include <vector>

using Point2D = Eigen::Matrix<double, 2, 1>;

class Position2D : public Eigen::Isometry2d {
public:
  Position2D(double x, double y, double theta) : Eigen::Isometry2d() {
    translation() << x, y;
    linear() = Eigen::Rotation2Dd(theta).toRotationMatrix();
  }
  Position2D(const Eigen::Isometry2d &other) : Eigen::Isometry2d(other) {}

  double X() const { return this->translation().x(); }
  double Y() const { return this->translation().y(); }
  double Theta() const { return Eigen::Rotation2Dd(linear()).angle(); }
};

class Polygon {
  using BoostPoint2D = boost::geometry::model::d2::point_xy<double>;
  using BoostPolygon = boost::geometry::model::polygon<BoostPoint2D>;

public:
  Polygon() = default;
  Polygon(const std::vector<Point2D> &vertices) {
    for (const auto &point : vertices) {
      boost::geometry::append(boostPolygon, BoostPoint2D(point.x(), point.y()));
    }
    boost::geometry::append(
        boostPolygon, BoostPoint2D(vertices.front().x(), vertices.front().y()));
  };

  BoostPolygon BoostPoly() const { return this->boostPolygon; }
  bool intersects(const Polygon &other) const {
    return boost::geometry::intersects(this->BoostPoly(), other.BoostPoly());
  }
  bool within(const Polygon &other) const {
    return boost::geometry::within(this->BoostPoly(), other.BoostPoly());
  }
  

private:
  BoostPolygon boostPolygon;
};

inline double degToRad(double angle) { return angle * M_PI / 180.0; }

inline double radToDeg(double angle) { return angle * 180.0 / M_PI; }

inline double wrapAngle(double angleRad) {
  return std::fmod(angleRad + M_PI, 2 * M_PI) - M_PI;
}