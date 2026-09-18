from Robot import robot

class drone(robot):
    def __init__(self, name: str, position: tuple, goal: tuple, distance: float, isFinished: bool, isSafe: bool, grid_dim: int):
        super().__init__(name, "drone", position, goal, distance, isFinished, grid_dim)
        self.isSafe = isSafe

            
    def isDroneSafe(self, other_robot: robot):
        if type(other_robot) == drone: # checks if the robot is a Drone
            if self.position == other_robot.position:
                # if the Drone is on another drone after moving, then it's not safe
                self.isSafe = False
            else:
                self.isSafe = True
        return self.isSafe
