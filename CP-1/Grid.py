from Robot import robot


class Grid:
    """Store objects by position and render them as a text grid."""

    def __init__(self, grid_dim: int):
        """
        Rows and columnsneed to be greater than 2 and less than 11.
        grid_dim is the dimension of the grid.  Only taken in once as the grid must be a square
        """

        self.rows = grid_dim
        self.columns = grid_dim
        self.positions = {} # this will store the positions of each robot where they currently are on the grid.  Updated by add_robot()
        self.timestamps = {} # this will hold self.positions for the i-th timestamp.  The timestamp will come from _main_ for each iteration
        self.robots = []

        num_robots = grid_dim * 2

        # initialize list of robots
        for i in range(num_robots):
            self.robots.append(robot.make_Robot(f'robot_{i}', grid_dim))

        # initialize positions dictionary
        for i in range(num_robots):
            self.positions[i] = self.robots[i].position

        

        self.timestamps[0] = self.positions # add the current positions to the first timestamp

    def add_robot(self):
        """
        This is mostly used to update grid.positions dictionary
        Add robots to the grid.positions dictionary
        """
        # for robot in list of positions
            # check if they're finished
            # if they're finished then call remove_robot
            # if they're not finished add them to grid.positions

    def move_robot(self):
        """Move robot to next position and check a lot of crap"""
        # find the next best position for the robot by calling the find_path
        # for loop to update robot positions
        # update grid.positions with all robot positions
        # check that there are no drones on drones, or humanoid/driver on humanoid/driver 
            # update positions with previous timestamp position if the above condition is not met

    def find_path(self):
        """
        Uses A* algorithm to find the best path from current robot position and map it to the goal

        Output will be the next position it needs to move to.  This will be called in move_robot to go to the next position.
        """
        # we will implement this last.  We should make sure we can generate the robots on to the grid first before getting this done.

    def remove_robot(self, robot):
        """Remove an object from the grid."""
        # check if robot.isFinished is True and remove it from the list of positions
        del self.positions[robot]

    def get_position(self, robot):
        """Return an object's ``(row, column)`` position."""
        row, column, _ = self.positions[robot]
        return row, column


def main():
    """Used for testing Grid class"""
    # create a grid
    grid_1= Grid(5)

    # print different components of the robots in the grid
    for robot in grid_1.robots:
        print(f'Name: {robot.name}, Type: {robot.robotype}, Position: {robot.position}, Goal: {robot.goal}, Distance:{robot.distance}, Finished: {robot.isFinished}')



    

if __name__ == "__main__":
    main()