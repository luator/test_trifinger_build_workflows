#!/usr/bin/env python3
"""Calibration of home offset for various finger robots."""
import argparse

import robot_interfaces
import test_trifinger_build_workflows


def main():
    robot_type = {
        "fingerone": (
            robot_interfaces.finger,
            test_trifinger_build_workflows.create_real_finger_backend,
            "finger.yml",
        ),
        "trifingerone": (
            robot_interfaces.trifinger,
            test_trifinger_build_workflows.create_trifinger_backend,
            "trifinger.yml",
        ),
        "fingeredu": (
            robot_interfaces.finger,
            test_trifinger_build_workflows.create_real_finger_backend,
            "fingeredu.yml",
        ),
        "trifingeredu": (
            robot_interfaces.trifinger,
            test_trifinger_build_workflows.create_trifinger_backend,
            "trifingeredu.yml",
        ),
        "trifingerpro": (
            robot_interfaces.trifinger,
            test_trifinger_build_workflows.create_trifinger_backend,
            "trifingerpro.yml",
        ),
    }

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("robot_type", choices=robot_type.keys())
    args = parser.parse_args()

    robot = test_trifinger_build_workflows.Robot(*robot_type[args.robot_type])

    print("")
    print("")
    input("Manually move robot to zero position.  Then press Enter.")
    robot.initialize()

    print("")
    print("Finished. The 'Offset' corresponds to the home offset.")


if __name__ == "__main__":
    main()
