import numpy as np
import random
import A_Star_basic as AS

# Robot class
    # roboType Drone subclass, Humanoid subclass, Driver subclass
    # position: current position tuple(x, y)
    # goal: Final position it's trying to reach tuple(x,y)
    # distance: Distance to the final position from the current position
    # isFinished: boolean of whether the robot position == goal
class robot:
    """
    Represents an individual robot.

    Each robot of roboType: Drone, Humanoid, Driver
    The position of the robot will be randomly generated based on a 5x5 grid
    The goal of the robot will also be randomly generated based on a 5x5 grid
    The distance is the euclidean distance between the robot position and goal
    isFinished is set as True when position = goal
    """
    def __init__(self, name, robotype, position, goal, distance, isFinished, grid_dim):
        # When Robot type is created, generate the roboType
        # GENERATE ROBOT FUNCTION
        self.name = name
        self.position = position
        self.robotype = robotype
        self.goal = goal
        self.distance = distance
        self.isFinished = isFinished
        self.grid_dim = grid_dim

        self.position = self.startPosition(grid_dim)
        self.goal = self.setGoal(grid_dim)
        
        self.distance = np.sqrt((self.goal[0]-self.position[0])**2 + (self.goal[1]-self.position[1])**2)

        self.path = AS.A_star(grid_dim, self.position, self.goal)

    @staticmethod
    def make_Robot(name, grid_dim):
        from Drone import drone
        from Humanoid import humanoid
        from Driver import driver

        robot_classes = (drone, humanoid, driver)
        robot_class = random.choice(robot_classes)
        distance = 0.0

        return robot_class(name, None, None, distance, False, True, grid_dim)


    def startPosition(self, n: int):
        """
        Generate positions at random based on the size of the grid being used

        Inputs:
            n(int): length of the grid dimension.  Grid must be n x n
        """
        rand_x = random.randrange(0, n)
        rand_y = random.randrange(0, n)
        return (rand_x, rand_y)

    def setGoal(self, n: int):
        """
        Generate positions at random based on the size of the grid being used

        Inputs:
            n(int): length of the grid dimension.  Grid must be n x n
        """
        rand_x = random.randrange(0, n)
        rand_y = random.randrange(0, n)
        goal = (rand_x, rand_y)
        if goal == self.position:
            return self.setGoal(n)
        
        return goal

    @staticmethod
    def safetyCheck(robot_1, robot_2):
        from Drone import drone
        from Humanoid import humanoid
        # from Driver import driver
        if robot_1.robotype == "drone":
            drone.isDroneSafe(robot_1, robot_2)
            return robot_1.isSafe
        if robot_1.robotype == "humanoid" or robot_1.robotype == "driver":
            humanoid.isHumanoidSafe(robot_1, robot_2)
            return robot_1.isSafe
        

def main():
    """Used for testing Robot class"""
    robo_1 = robot.make_Robot("Robot_1", 5)
    print(type(robo_1))
    print(robo_1.name)
    print(robo_1.position)
    print(robo_1.goal)
    

if __name__ == "__main__":
    main()