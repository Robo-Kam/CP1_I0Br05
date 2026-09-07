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
class Robot:
    """
    Represents an individual robot.

    Each robot of roboType: Drone, Humanoid, Driver
    The position of the robot will be randomly generated based on a 5x5 grid
    The goal of the robot will also be randomly generated based on a 5x5 grid
    The distance is the euclidean distance between the robot position and goal
    isFinished is set as True when position = goal
    """
    def __init__(self, roboType, position, goal, distance, isFinished):

        # When Robot type is created, generate the roboType
        self.roboType = random.randrange(0,2)
        if self.roboType == 0:
            self.roboType = Drone
        if self.roboType == 1:
            self.roboType = Humanoid
        if self.roboType == 2:
            self.roboType = Driver
        
        self.position = self.startPosition()
        self.goal = self.setGoal()
        self.distance = np.sqrt((self.goal[0]-self.position[0])**2 + (self.goal[1]-self.position[1])**2)

        if self.position[0] == self.goal[0] and self.position[1] == self.goal[1]:
            self.isFinished == True
        else:
            self.isFinished == False

    def startPosition(self, length_grid_x, length_grid_y):
        rand_x = random.randrange(0, length_grid_x)
        rand_y = random.randrange(0, length_grid_y)
        self.position = (rand_x, rand_y)

