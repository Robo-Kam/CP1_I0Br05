<<<<<<< HEAD
# Driver subclass
    # onHumanoid: boolean of whether the humanoid is on another humanoid
    # onDriver: boolean of whether the humanoid is on a Driver
=======
from Robot import robot

class driver(robot):
    def __init__(self, name: str, position: tuple, goal: tuple, distance: float, isFinished: bool, isSafe: bool, grid_dim: int):
        super().__init__(name, "driver", position, goal, distance, isFinished, grid_dim)
        self.isSafe = isSafe
            
    def isDriverSafe(self, other_robot: robot):
        from Humanoid import humanoid

        if type(other_robot) == driver or type(other_robot) == humanoid: # checks if the robot is a Driver or humanoid
            if self.position == other_robot.position:
                # if the Driver is on the same spot as another driver or humanoid
                self.isSafe = False
            else:
                self.isSafe = True
        return self.isSafe
>>>>>>> Grid_Test
