#pragma once

#include "ompl/base/PlannerData.h"
#include "planners/planner_interface.hpp"
#include "robot_state.hpp"
#include "utils/geometry.hpp"
#include "utils/logger.hpp"
#include <fstream>
#include <ompl/base/spaces/SE2StateSpace.h>
#include <ompl/geometric/SimpleSetup.h>
#include <ompl/geometric/planners/prm/PRMstar.h>
#include <ompl/geometric/planners/rrt/RRTstar.h>
#include <ompl/geometric/planners/rrt/RRTConnect.h>
#include <ompl/geometric/planners/fmt/FMT.h>
#include <ompl/geometric/planners/informedtrees/BITstar.h>


using PRMStar = ompl::geometric::PRMstar;
using RRTStar = ompl::geometric::RRTstar;
using RRTConnect = ompl::geometric::RRTConnect;
using FMT = ompl::geometric::FMT;
using BITStar = ompl::geometric::BITstar;


template<typename PlannerType>
class OMPLPlanner : public PlannerInterface{
public:
  OMPLPlanner(std::shared_ptr<LoggerInterface> logger)
      : PlannerInterface(), logger(logger){};

  PlanningResult plan() override {
    auto map_space = std::make_shared<ompl::base::SE2StateSpace>();

    ompl::base::RealVectorBounds map_bounds(2);

    map_bounds.setLow(0, 0.0);
    map_bounds.setHigh(0, this->map->config().width);
    map_bounds.setLow(1, 0.0);
    map_bounds.setHigh(1, this->map->config().height);

    map_space->setBounds(map_bounds);

    this->logger->log("Robot size: " + std::to_string(this->robotSize.length) +
                      ", " + std::to_string(this->robotSize.width));

    this->logger->log("Start: " + std::to_string(this->start.X()) + ", " +
                      std::to_string(this->start.Y()) + ", " +
                      std::to_string(this->start.Theta()));

    this->logger->log("Goal: " + std::to_string(this->goal.X()) + ", " +
                      std::to_string(this->goal.Y()) + ", " +
                      std::to_string(this->goal.Theta()));

    ompl::base::ScopedState<> start_point_state(map_space);
    ompl::base::ScopedState<> goal_point_state(map_space);
    stateToOmplState(this->start, start_point_state());
    stateToOmplState(this->goal, goal_point_state());

    ompl::geometric::SimpleSetup planner_task(map_space);
    planner_task.setStateValidityChecker(
        [this](const ompl::base::State *omplState) {
          return this->map->checkStateConsistency(
              RobotState(this->robotSize, omplStateToState(omplState)));
        });

    planner_task.setPlanner(std::make_shared<PlannerType>(
        planner_task.getSpaceInformation()));

    planner_task.setStartAndGoalStates(start_point_state, goal_point_state);
    planner_task.setup();
    auto is_task_solved = planner_task.solve(5);

    if (is_task_solved) {
      this->logger->log("Path found");
      std::ofstream output("planner_solution.txt");
      std::ofstream graph("graph.txt");
      auto pd = ompl::base::PlannerData(planner_task.getSpaceInformation());
      planner_task.getSolutionPath().printAsMatrix(output);
      planner_task.getPlannerData(pd);
      pd.printPLY(graph);
      return PlanningResult::SUCCESS;
    } else {
      this->logger->log("Path not found");
      return PlanningResult::PATH_NOT_FOUND;
    }
  }

private:
  void stateToOmplState(Position2D position, ompl::base::State *omplState) {
    omplState->as<ompl::base::SE2StateSpace::StateType>()->setX(position.X());
    omplState->as<ompl::base::SE2StateSpace::StateType>()->setY(position.Y());
    omplState->as<ompl::base::SE2StateSpace::StateType>()->setYaw(
        position.Theta());
  }

  Position2D omplStateToState(const ompl::base::State *omplState) {
    return Position2D{
        omplState->as<ompl::base::SE2StateSpace::StateType>()->getX(),
        omplState->as<ompl::base::SE2StateSpace::StateType>()->getY(),
        wrapAngle(
            omplState->as<ompl::base::SE2StateSpace::StateType>()->getYaw()),
    };
  }

private:
  std::shared_ptr<LoggerInterface> logger;
};
