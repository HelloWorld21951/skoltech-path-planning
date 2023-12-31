#include "planners_server.hpp"
#include <rclcpp/rclcpp.hpp>

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<rclcpp::Node>("planners_node");
  auto plannersServer = std::make_shared<PlannersServer>(node);
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}