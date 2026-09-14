from Robot import robot
from Driver import driver

class humanoid(robot):
    def __init__(self, name: str, position: tuple, goal: tuple, distance: float, isFinished: bool, isSafe: bool, grid_dim: int):
        super().__init__(name, "humanoid", position, goal, distance, isFinished, grid_dim)
        self.isSafe = isSafe

    def isHumanoidSafe(self, other_robot: robot):
        if type(other_robot) == driver or type(other_robot) == humanoid: # checks if the robot is a Driver or humanoid
            if self.position == other_robot.position:
                # if the Driver is on the same spot as another driver or humanoid
                self.isSafe = False
            else:
                self.isSafe = True
        return self.isSafe