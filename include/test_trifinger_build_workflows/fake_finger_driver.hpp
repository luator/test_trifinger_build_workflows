#pragma once

#include <chrono>
#include <thread>

#include <Eigen/Eigen>

#include <test_trifinger_build_workflows/n_joint_blmc_robot_driver.hpp>
#include <robot_interfaces/finger_types.hpp>

namespace test_trifinger_build_workflows
{
// TODO rename to include "Mono"
class FakeFingerDriver : public robot_interfaces::RobotDriver<
                             robot_interfaces::MonoFingerTypes::Action,
                             robot_interfaces::MonoFingerTypes::Observation>
{
public:
    typedef robot_interfaces::MonoFingerTypes::Action Action;
    typedef robot_interfaces::MonoFingerTypes::Observation Observation;
    typedef robot_interfaces::MonoFingerTypes::Action::Vector Vector;

    int data_generating_index_ = 0;

    FakeFingerDriver()
    {
    }

    Observation get_latest_observation() override
    {
        // generating observations by a rule to make it easier to check they are
        // being logged correctly as the timeindex increases.

        Observation observation;
        observation.position[0] = data_generating_index_;
        observation.position[1] = 2 * data_generating_index_;
        observation.position[2] = 3 * data_generating_index_;

        observation.velocity[0] = data_generating_index_ + 1;
        observation.velocity[1] = 2 * data_generating_index_ + 1;
        observation.velocity[2] = 3 * data_generating_index_ + 1;

        observation.torque[0] = data_generating_index_ + 2;
        observation.torque[1] = 2 * data_generating_index_ + 2;
        observation.torque[2] = 3 * data_generating_index_ + 2;

        observation.tip_force[0] = data_generating_index_ / 2;

        data_generating_index_++;

        return observation;
    }

    Action apply_action(const Action &desired_action) override
    {
        using namespace std::chrono_literals;
        std::this_thread::sleep_for(1ms);

        return desired_action;
    }

    std::optional<std::string> get_error() override
    {
        return std::nullopt;  // no errors
    }

    void shutdown() override
    {
        return;
    }

    void initialize() override
    {
        return;
    }
};

robot_interfaces::MonoFingerTypes::BackendPtr create_fake_finger_backend(
    robot_interfaces::MonoFingerTypes::BaseDataPtr robot_data)
{
    auto robot = std::make_shared<FakeFingerDriver>();
    auto backend = std::make_shared<robot_interfaces::MonoFingerTypes::Backend>(
        robot, robot_data);
    backend->set_max_action_repetitions(-1);

    return backend;
}

}  // namespace test_trifinger_build_workflows
