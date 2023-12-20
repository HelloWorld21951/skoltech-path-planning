cmake_minimum_required(VERSION 3.8)
project(sampling_based_planners)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
  if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
  endif()

  set(CMAKE_CXX_FLAGS_DEBUG "-g -march=native")
  set(CMAKE_CXX_FLAGS_RELEASE "-O3 -march=native")
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(ompl REQUIRED)
find_package(eigen3_cmake_module REQUIRED)
find_package(Eigen3 REQUIRED)

file(GLOB_RECURSE PLANNER_SOURCES "src/*.cpp")

add_executable(planners_node 
  ${PLANNER_SOURCES}
)

ament_target_dependencies(planners_node
  rclcpp
  geometry_msgs
  ompl
  eigen3_cmake_module
  Eigen3
)

target_include_directories(planners_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

target_compile_features(planners_node PUBLIC cxx_std_17)

include_directories(
  include 
  ${OMPL_INCLUDE_DIRS}
)

target_link_libraries(planners_node
  ${OMPL_LIBRARIES}
)

install(TARGETS 
  planners_node
  DESTINATION lib/${PROJECT_NAME})

install(DIRECTORY
  launch
  config
  scripts
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
