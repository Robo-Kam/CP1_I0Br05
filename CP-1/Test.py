from Grid import Grid

class Robot:
    symbol = "R"

robot = Robot()
grid = Grid()
grid.add_object(robot, 1, 2)
assert grid.get_position(robot) == (1, 2)
assert grid.render().splitlines()[1] == ". . R . ."
grid.move_object(robot, 3, 4)
assert grid.get_position(robot) == (3, 4)
assert grid.render().splitlines()[3] == ". . . . R"
print(grid)
