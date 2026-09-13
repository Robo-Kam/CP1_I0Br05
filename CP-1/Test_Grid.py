"""Plot Robot movement from each start position to each goal."""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle

from Driver import Driver
from Drone import Drone
from Humanoid import Humanoid
from Robot import Robot

n=10

class Grid:
    """Store Robot positions as timestamps while they move to their goals."""

    def __init__(self, rows=n, columns=n):
        self.rows = rows
        self.columns = columns
        self.robots = []
        self.history = []

    def add_robot(self, robot):
        """Add a Robot and save the initial timestamp."""
        # if robot.position in [item.position for item in self.robots]:
        #     raise ValueError("Two robots cannot share a position")
        self.robots.append(robot)
        self.history.append(self._snapshot())

    def _snapshot(self):
        return [
            {
                "type": robot.roboType.__name__,
                "position": tuple(robot.position),
                "goal": tuple(robot.goal),
            }
            for robot in self.robots
        ]

    def _next_position(self, position, goal):
        row, column = position
        goal_row, goal_column = goal

        if row != goal_row:
            row += 1 if goal_row > row else -1
        elif column != goal_column:
            column += 1 if goal_column > column else -1
        return row, column

    def advance(self):
        """Move every Robot one square toward its goal."""
        for robot in self.robots:
            if robot.position != robot.goal:
                robot.position = self._next_position(robot.position, robot.goal)

        self.history.append(self._snapshot())

    def run(self):
        """Create timestamps until all Robots reach their goals."""
        while any(robot.position != robot.goal for robot in self.robots):
            self.advance()

    def timestamp(self, index):
        return self.history[index]


def draw_shape(ax, row, column, robot_type, rows):
    """Draw one Robot type at its current position."""
    center_x = column + 0.5
    center_y = rows - row - 0.5

    if robot_type == "Driver":
        ax.add_patch(Circle((center_x, center_y), 0.15, color="steelblue"))
    elif robot_type == "Drone":
        ax.add_patch(Rectangle(
            (center_x - 0.15, center_y - 0.15),
            0.3,
            0.3,
            color="tomato",
        ))
    elif robot_type == "Humanoid":
        points = [
            (center_x, center_y + 0.15),
            (center_x - 0.15, center_y - 0.15),
            (center_x + 0.15, center_y - 0.15),
        ]
        ax.add_patch(Polygon(points, color="seagreen"))


def create_grid(n):
    """Create Robots, add them to a Grid, and generate all timestamps."""
    robots = []
    for i in range(n):
        robot = Robot()
        robots.append(robot)
        print(
            f"Robot {i + 1}: Type={robot.roboType.__name__}, "
            f"Position={robot.position}, Goal={robot.goal}, "
            f"Distance={robot.distance:.2f}, Finished={robot.isFinished}"
        )
    grid = Grid()
    for robot in robots:
        grid.add_robot(robot)
    grid.run()
    return grid


def plot_grid(grid):
    """Plot Grid timestamps and switch between them with keyboard input."""
    fig, ax = plt.subplots()
    current_timestamp = 0

    def draw_update(timestamp):
        ax.clear()
        ax.set_xlim(0, grid.columns)
        ax.set_ylim(0, grid.rows)
        ax.set_xticks(range(grid.columns + 1))
        ax.set_yticks(range(grid.rows + 1))
        ax.grid(True)
        ax.set_aspect("equal")
        ax.set_title(f"Timestamp {timestamp + 1} of {len(grid.history)}")

        for state in grid.timestamp(timestamp):
            row, column = state["position"]
            goal_row, goal_column = state["goal"]
            current_x, current_y = column + 0.5, grid.rows - row - 0.5
            goal_x, goal_y = goal_column + 0.5, grid.rows - goal_row - 0.5

            ax.plot(
                [current_x, goal_x],
                [current_y, goal_y],
                color="gray",
                linestyle="--",
                linewidth=1.5,
                zorder=1,
            )
            draw_shape(ax, row, column, state["type"], grid.rows)

        fig.canvas.draw_idle()

    def toggle_update(event):
        nonlocal current_timestamp
        if event.key in ("right", " "):
            current_timestamp = min(current_timestamp + 1, len(grid.history) - 1)
        elif event.key == "left":
            current_timestamp = max(current_timestamp - 1, 0)
        else:
            return
        draw_update(current_timestamp)

    draw_update(current_timestamp)
    fig.canvas.mpl_connect("key_press_event", toggle_update)
    plt.show()


def main():
    plot_grid(create_grid(n=10))
    print(Grid.timestamps)

if __name__ == "__main__":
    main()