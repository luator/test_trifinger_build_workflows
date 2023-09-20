#!/usr/bin/env python3
"""Send zero-torque commands to the robot and print joint positions."""
import argparse

import test_trifinger_build_workflows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "robot_type", choices=test_trifinger_build_workflows.Robot.get_supported_robots()
    )
    args = parser.parse_args()

    robot = test_trifinger_build_workflows.Robot.create_by_name(args.robot_type)

    robot.initialize()
    test_trifinger_build_workflows.demo_print_position(robot)


if __name__ == "__main__":
    main()
