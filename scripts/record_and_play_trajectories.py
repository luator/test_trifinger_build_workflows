#!/usr/bin/env python3
"""Record data while the user is manually moving the robot."""
import numpy as np
import test_trifinger_build_workflows
import typing


def record(trajectory: typing.List[np.ndarray]):
    trajectory[:] = []
    t = 0
    while True:
        t = robot.frontend.append_desired_action(robot.Action())
        robot.frontend.wait_until_timeindex(t)
        trajectory += [robot.frontend.get_observation(t).position]

        if len(trajectory) > 3000:
            if np.abs(trajectory[-1] - trajectory[-2000]).sum() < 0.01:
                return


def play(trajectory: typing.List[np.ndarray], factor: int):
    for position in trajectory[::factor]:
        action = robot.Action(position=position)
        t = robot.frontend.append_desired_action(action)
        robot.frontend.wait_until_timeindex(t - 10)

    robot.frontend.append_desired_action(robot.Action())


if __name__ == "__main__":
    robot = test_trifinger_build_workflows.Robot.create_by_name("trifingerpro")
    robot.initialize()

    trajectory: typing.List[np.ndarray] = []
    while True:
        print("enter key")
        key = input()
        if key == "r":
            print("recording")
            record(trajectory)
        elif key in list(map(str, range(1, 20))):
            print("playing with factor " + key)
            play(trajectory, int(key))
        else:
            print("invalid key")
