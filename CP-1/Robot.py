import numpy as np
import random
from Drone import Drone
from Humanoid import Humanoid
from Driver import Driver

# Robot class
    # roboType Drone subclass, Humanoid subclass, Driver subclass
    # position: current position tuple(x, y)
    # goal: Final position it's trying to reach tuple(x,y)
    # distance: Distance to the final position from the current position
    # isFinished: boolean of whether the robot position == goal

n=10

class Robot:
    """
    Represents an individual robot.

    Each robot of roboType: Drone, Humanoid, Driver
    The position of the robot will be randomly generated based on a nxn grid
    The goal of the robot will also be randomly generated based on a nxn grid
    The distance is the euclidean distance between the robot position and goal
    isFinished is set as True when position = goal
    """
    def __init__(self, roboType=None, position=None, goal=None,
                 distance=None, isFinished=None):
        """Create a robot, generating any values that were not supplied."""
        self.roboType = roboType or random.choice((Drone, Humanoid, Driver))
        self.position = position if position is not None else self.startPosition()
        self.goal = goal if goal is not None else self.setGoal()
        self.distance = (
            distance if distance is not None else self._calculate_distance()
        )
        self.isFinished = (
            isFinished if isFinished is not None else self.position == self.goal
        )
    
    def startPosition(self, length_grid_x=n, length_grid_y=n):
        rand_x = random.randrange(length_grid_x)
        rand_y = random.randrange(length_grid_y)
        return rand_x, rand_y

    def setGoal(self, length_grid_x=n, length_grid_y=n):
        return self.startPosition(length_grid_x, length_grid_y)

    def _calculate_distance(self):
        return np.sqrt(
            (self.goal[0] - self.position[0]) ** 2
            + (self.goal[1] - self.position[1]) ** 2
        )

    
def main():
 n=10
 for i in range(n*2):
        robot = Robot()
        print(
            f"Robot {i+1}: Type={robot.roboType.__name__}, "
            f"Position={robot.position}, Goal={robot.goal}, "
            f"Distance={robot.distance:.2f}, Finished={robot.isFinished}"
        )


if __name__ == "__main__":
    main()