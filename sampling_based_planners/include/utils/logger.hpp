#pragma once

#include <memory>
#include <rclcpp/logger.hpp>
#include <rclcpp/node.hpp>
#include <string>

class LoggerInterface {
public:
  virtual void log(const std::string &msg) = 0;
};

class RosLogger : public LoggerInterface {
public:
  RosLogger(rclcpp::Node::SharedPtr node)
      : LoggerInterface(),
        logger(std::make_shared<rclcpp::Logger>(node->get_logger())){};
  void log(const std::string &msg) override {
    RCLCPP_INFO(*this->logger, "%s", msg.c_str());
  };

private:
  std::shared_ptr<rclcpp::Logger> logger;
};