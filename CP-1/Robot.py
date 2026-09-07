# Robot class
    # type: Drone subclass, Humanoid subclass, Driver subclass
    # position: current position tuple(x, y)
    # goal: Final position it's trying to reach tuple(x,y)
    # distance: Distance to the final position from the current position
    # isFinished: boolean of whether the robot position == goal

# Drone subclass
    # onDrone: boolean of whether the drone is in the same position as another
        # result of method iterating through all other Drone positions that are not 'isFinished'

# Humanoid subclass
    # onHumanoid: boolean of whether the humanoid is on another humanoid
    # onDriver: boolean of whether the humanoid is on a Driver

# Driver subclass
    # onHumanoid: boolean of whether the humanoid is on another humanoid
    # onDriver: boolean of whether the humanoid is on a Driver