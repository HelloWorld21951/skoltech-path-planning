#pragma once

#include "rclcpp/rclcpp.hpp"
#include <rclcpp/parameter.hpp>

template <typename T>
T getParameter(rclcpp::Node::SharedPtr node, const std::string &name) {
  if (!node->has_parameter(name)) {
    node->declare_parameter<T>(name);
  }
  const auto param = node->get_parameter(name);
  RCLCPP_INFO(node->get_logger(), "Init parameter %s with value %s",
              name.c_str(), param.value_to_string().c_str());
  return param.get_parameter_value().get<T>();
}