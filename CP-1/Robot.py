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

        self.position = self.startPosition(grid_dim) # generate random starting position within the grid
        self.goal = self.setGoal(grid_dim) # generate random goal position within the grid.  Cannot be the same as starting position
        
        self.distance = np.sqrt((self.goal[0]-self.position[0])**2 + (self.goal[1]-self.position[1])**2) # initial euclidean distance between start and goal

        self.path = AS.A_star(grid_dim, self.position, self.goal) # A* path planning algorithm.  Uses euclidean distance heuristic.  Cost is only 1 for each step.

    @staticmethod
    def make_Robot(name, grid_dim):
        """
        Generates a robot of random type.  Method is static, because it's called in the grid class, 
        which is where the input is received for the grid dimension.
        Inputs:
            name(str): name of the robot
            grid_dim(int): length of the grid dimension (n).
        Output:
            robot_class: a randomly generated robot of type drone, humanoid, or driver
        """
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

    def checkFinished(self):
        """
        Check if the robot has reached its goal. If it has, then change isFinished to True.
        """
        if self.position == self.goal:
            self.isFinished = True
        else:
            self.isFinished = False

    @staticmethod
    def safetyCheck(robot_1, robot_2):
        """
        This function is used in the conditional check.  This specific one pulls
        the subclass functions to check if the robot is in the same position as an incompatible robot.
        The function returns a boolean value to move the conditional_check function to the next step.
        In the simplest case it just compares two robots and checks if they are compatible.
        Inputs:
            robot_1 (drone, humanoid, driver): first robot in comparison
            robot_2 (drone, humanoid, driver): second robot in comparison
        Outputs:
            isSafe (bool): True is they are compatible, False if they are not.
        """
        from Drone import drone
        from Humanoid import humanoid
        from Driver import driver
        if type(robot_1) == drone:
            drone.isDroneSafe(robot_1, robot_2)
            return robot_1.isSafe
        elif type(robot_1) == driver:
            driver.isDriverSafe(robot_1, robot_2)
            return robot_1.isSafe
        else:
            humanoid.isHumanoidSafe(robot_1, robot_2)
            return robot_1.isSafe
        

def main():
    """Used for testing Robot class.  Below is an example of how to create a robot"""
    robo_1 = robot.make_Robot("Robot_1", 5)
    print(f'NAME: {robo_1.name}')
    print(f'TYPE: {type(robo_1)}')
    print(f'POSITION: {robo_1.position}')
    print(f'GOAL: {robo_1.goal}')
    print(f'DISTANCE: {robo_1.distance}')
    print(f'ISFINISHED: {robo_1.isFinished}')
    print(f'GRID_DIM: {robo_1.grid_dim}')
    

if __name__ == "__main__":
    main()