"""Plot robot movement and one synchronized planning grid per robot."""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle

from Robot import robot

#placeholder value for grid/robot inputs
n=5
class Grid:
    """Store robot positions at each simulation timestamp."""

    def __init__(self, grid_size):
        self.rows = grid_size
        self.columns = grid_size
        self.robots = []
        self.history = []

    def add_robot(self, new_robot):
        self.robots.append(new_robot)

    def _snapshot(self):
        """Base Function for creating inputs for robot plotting"""
        return [
            {
                "name": new_robot.name,
                "type": type(new_robot).__name__,
                "position": tuple(new_robot.position),
                "goal": tuple(new_robot.goal),
            }
            for new_robot in self.robots
        ]

    @staticmethod
    def _next_position(position, path):
        """Return the next waypoint from the robot's A* path."""
        if not path:
            return position
        if position not in path:
            return path[0]
        path_index = path.index(position)
        return path[min(path_index + 1, len(path) - 1)]

    def run(self):
        """Generate timestamps until every robot reaches its goal."""
        self.history.append(self._snapshot())
        while any(new_robot.position != new_robot.goal for new_robot in self.robots):
            for new_robot in self.robots:
                if new_robot.position != new_robot.goal:
                    new_robot.position = self._next_position(
                        new_robot.position, new_robot.path
                    )
            self.history.append(self._snapshot())


    def timestamp(self, index):
        """Indexes timestamps for robots"""
        return self.history[index]

 
                


def draw_shape(axis, row, column, robot_type, grid_size, color, filled=True):
    """Draw a robot marker and its goal position."""
    center_x = column + 0.5
    center_y = grid_size - row - 0.5
    face_color = color if filled else "none"
    if robot_type == "driver":
        axis.add_patch(
            Circle((center_x, center_y), 0.15, facecolor=face_color, edgecolor=color)
        )
    elif robot_type == "humanoid":
        axis.add_patch(
            Rectangle(
                (center_x - 0.15, center_y - 0.15),
                0.3,
                0.3,
                facecolor=face_color,
                edgecolor=color,
            )
        )
    elif robot_type == "drone":
        axis.add_patch(
            Polygon(
                [
                    (center_x, center_y + 0.15),
                    (center_x - 0.15, center_y - 0.15),
                    (center_x + 0.15, center_y - 0.15),
                ],
                facecolor=face_color,
                edgecolor=color,
            )
        )


def draw_grid(axis, grid_size):
    """"""
    for coordinate in range(grid_size + 1):
        axis.plot([0, grid_size], [coordinate, coordinate], color="lightgray", linewidth=0.8)
        axis.plot([coordinate, coordinate], [0, grid_size], color="lightgray", linewidth=0.8)


def create_grid(grid_size=n, robot_count=n*2):
    grid = Grid(grid_size)
    for index in range(robot_count):
        new_robot = robot.make_Robot(f"Robot {index + 1}", grid_size)
        grid.add_robot(new_robot)
    grid.run()
    return grid


def plot_grid(grid):
    """Function set for displaying a robot number planning plot and a timestamp plot for all robots.
    """
    if not grid.robots:
        raise ValueError("The grid must contain at least one robot")

    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]
    figure, axis = plt.subplots(figsize=(6, 6))
    timestamp_figure, timestamp_axis = plt.subplots(figsize=(6, 6))
    robot_num = 0
    current_timestamp = 0

    def planned_path(new_robot):
        """Return the A* path with the robot's initial position included."""
        # if not new_robot.path:
        #     raise ValueError(f"{new_robot.name} has not path")

        path = list(new_robot.path)
        initial_state = next(
            state for state in grid.history[0] if state["name"] == new_robot.name
        )
        initial_position = initial_state["position"]
        if path[0] != initial_position:
            path.insert(0, initial_position)

        return path
    
    def draw_robot_grid():
        """Path Planning Graph for n*2 number of Robots"""
        new_robot = grid.robots[robot_num]
        axis.clear()
        draw_grid(axis, grid.columns)
        path = planned_path(new_robot)
        color = colors[robot_num % len(colors)]
        axis.plot(
            [column + 0.5 for row, column in path],
            [grid.rows - row - 0.5 for row, column in path],
            color=color,
            linewidth=3,
        )
        start_row, start_column = path[0]
        goal_row, goal_column = path[-1]
        draw_shape(
            axis,
            start_row,
            start_column,
            type(new_robot).__name__,
            grid.rows,
            color,
        )
        draw_shape(
            axis,
            goal_row,
            goal_column,
            type(new_robot).__name__,
            grid.rows,
            color,
            filled=False,
        )
        axis.set_xlim(0, grid.columns)
        axis.set_ylim(0, grid.rows)
        axis.set_aspect("equal")
        axis.set_title(f" {new_robot.name} Type: {new_robot.robotype}")
        axis.set_xlabel(f"Path to goal {new_robot.goal}")
        #figure.suptitle(f"Planning path, robot_num = {robot_num + 1}")
        figure.tight_layout()
        figure.canvas.draw_idle()

    def draw_timestamp():
        """Plot for drawing robots to goal with euclidian distance as the line between"""
        timestamp_axis.clear()
        draw_grid(timestamp_axis, grid.columns)
        for index, state in enumerate(grid.timestamp(current_timestamp)):
            row, column = state["position"]
            goal_row, goal_column = state["goal"]

            ##Redoes not plot robot if position=goal
            # if state["position"] == state["goal"]:
            #     continue
            color = colors[index % len(colors)]
            timestamp_axis.plot(
                [column + 0.5, goal_column + 0.5],
                [grid.rows - row - 0.5, grid.rows - goal_row - 0.5],
                color="gray",
                linestyle="--",
                linewidth=1.5,
            )
            #Section for Drawing shapes based on robotype
            draw_shape(
                timestamp_axis,
                row,
                column,
                state["type"],
                grid.rows,
                color,
            )
            draw_shape(
                timestamp_axis,
                goal_row,
                goal_column,
                state["type"],
                grid.rows,
                color,
                filled=False,
            )
        timestamp_axis.set_xlim(0, grid.columns)
        timestamp_axis.set_ylim(0, grid.rows)
        timestamp_axis.set_aspect("equal")
        #timestamp_axis.legend(loc='upper right', )
        timestamp_axis.set_title(
            f"Robot timestamps: {current_timestamp + 1} of {len(grid.history)}"
        )

        timestamp_figure.tight_layout()
        timestamp_figure.canvas.draw_idle()

    def update(event):
        """Method for controlling the updated timestamps with keyboard inputs"""
        nonlocal current_timestamp, robot_num
        if event.canvas == timestamp_figure.canvas:
            if event.key in ("right", " ", "pagedown"):
                current_timestamp = min(current_timestamp + 1, len(grid.history) - 1)
            elif event.key in ("left", "pageup"):
                current_timestamp = max(current_timestamp - 1, 0)
            else:
                return
            draw_timestamp()
        else:
            if event.key in ("right", " ", "pagedown"):
                robot_num = min(robot_num + 1, len(grid.robots) - 1)
            elif event.key in ("left", "pageup"):
                robot_num = max(robot_num - 1, 0)
            else:
                return
            draw_robot_grid()

    draw_robot_grid()
    draw_timestamp()
    figure.canvas.mpl_connect("key_press_event", update)
    timestamp_figure.canvas.mpl_connect("key_press_event", update)
    plt.show()


if __name__ == "__main__":
    # nu=int(input("Set Grid Size, n \n"))
    # print("\nDrone: Triangle \n" \
    # "Humanoid: Square \n" \
    # "Driver: Circle")
    nu=10
    grid = create_grid(grid_size=nu,robot_count=nu*2)
    ##Debug for printing timestamps
    # for index, snapshot in enumerate(grid.history):
    #     print(f"Timestamp {1}: {snapshot[1]['name']} {snapshot[1]['position']} \n\n\n ")
    
    for new_robot in grid.robots:
        print(f"{new_robot.name}:start: {new_robot.path[0]} goal:{new_robot.goal} path: {new_robot.path}")

    plot_grid(grid)
 
