cmake_minimum_required(VERSION 3.8)
project(sampling-based-planners)

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
find_package(ompl REQUIRED)

file(GLOB_RECURSE PLANNER_SOURCES "src/*.cpp")

add_executable(sampling_based_planners 
  ${PLANNER_SOURCES}
)

ament_target_dependencies(sampling_based_planners
  rclcpp
  ompl
)

target_include_directories(sampling_based_planners PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

target_compile_features(sampling_based_planners PUBLIC cxx_std_17)

include_directories(
  include 
  ${OMPL_INCLUDE_DIRS}
)

target_link_libraries(sampling_based_planners
  ${OMPL_LIBRARIES}
)

install(TARGETS 
  sampling_based_planners
  DESTINATION lib/${PROJECT_NAME})

install(DIRECTORY
  launch
  config
  scripts
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
