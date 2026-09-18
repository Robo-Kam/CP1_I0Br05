from Robot import robot


class Grid:
    """Store objects by position and render them as a text grid."""

    def __init__(self, grid_dim: int):
        """
        Rows and columns need to be greater than 2 and less than 11.
        grid_dim is the dimension of the grid.  Only taken in once as the grid must be a square
        """

        self.rows = grid_dim
        self.columns = grid_dim
        self.positions = {} # this will store the positions of each robot where they currently are on the grid.  Updated by add_robot()
        self.timestamps = {} # this will hold self.positions for the i-th timestamp.  The timestamp will come from _main_ for each iteration
        self.robots = [] # stores the generated list of robots
        self.path = {} # stores the paths for each of the robots

        num_robots = grid_dim * 2

        # initialize list of robots
        for i in range(num_robots):
            self.robots.append(robot.make_Robot(f'robot_{i}', grid_dim))# make grid_dim * 2 number of robots and name them robot_1, robot_2, robot_3, ...

        # initialize positions dictionary
        for i in range(num_robots):
            self.positions[i] = self.robots[i].position       

        self.timestamps[0] = self.positions # add the start positions to the first timestamp


# used for testing
def main():
    """Used for testing Grid class"""
    # create a grid.  This generates all of the required robots with their start positions, goal and pathing.
    grid_1= Grid(5)

    # print different components of the robots in the grid
    for robot in grid_1.robots:
        print(f'Name: {robot.name}, Type: {robot.robotype}, Position: {robot.position}, Goal: {robot.goal}, Distance:{robot.distance}, Finished: {robot.isFinished}')
        print(f'Path:{robot.path}')

# run main for testing
if __name__ == "__main__":
    main()