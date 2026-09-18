import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from A_Star_basic import A_star

def draw_grid(ax, n, color="lightgray", linewidth=0.8):
    """Draw the nxn grid lines."""
    for i in range(n + 1):
        ax.plot([0, n], [i, i], color=color, linewidth=linewidth)
        ax.plot([i, i], [0, n], color=color, linewidth=linewidth)


def draw_robot_path(ax, path, color="tab:blue", label=None):
    """Draw a robot path as filled square cells on the grid."""
    if not path:
        return

    for row, col in path:
        rect = Rectangle(
            (col, row),
            1,
            1,
            facecolor="none",
            edgecolor=color,
            linewidth=2,
            label=label if row == path[0][0] and col == path[0][1] else None,
        )
        ax.add_patch(rect)

    start = path[0]
    goal = path[-1]
    ax.plot(start[1] + 0.5, start[0] + 0.5, "s", color=color, markersize=8)
    ax.plot(goal[1] + 0.5, goal[0] + 0.5, "s", color=color, markersize=8,fillstyle="none",markeredgewidth=2)


def plot_robot_paths(robot_paths, grid_size, colors=None):
    """Plot one or many robot paths on the same grid."""
    if colors is None:
        colors = ["tab:blue", "tab:orange", "tab:green", "tab:red"]

    fig, ax = plt.subplots(figsize=(6, 6))
    draw_grid(ax, grid_size)

    for i, path in enumerate(robot_paths):
        color = colors[i % len(colors)]
        draw_robot_path(ax, path, color=color, label=f"Robot {i + 1}")

    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)
    ax.set_aspect("equal")
    ax.set_xticks(range(grid_size + 1))
    ax.set_yticks(range(grid_size + 1))
    ax.set_title("Robot paths")
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    ax.legend(loc="upper right")
    plt.show()





def plot_grid(grid):
    """Plot Grid timestamps and switch between them with keyboard input."""
    fig, ax = plt.subplots()
    current_robot = 0

    def draw_path_update(robot_num):
        ax.set_xlim(0, grid_size=griddie)
        ax.set_ylim(0, grid_size=griddie)
        ax.set_aspect("equal")
        ax.set_xticks(range(grid_size=griddie + 1))
        ax.set_yticks(range(grid_size=griddie + 1))
        ax.set_xlabel("Column")
        ax.set_ylabel("Row")
        ax.legend(loc="upper right")
        ax.set_title(f"Robot {robot_num + 1} of {len(grid.history)}")

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
            """Show robot timestamps and planned paths in two synchronized windows."""

            import matplotlib.pyplot as plt
            from matplotlib.patches import Circle, Polygon, Rectangle

            from A_Star_basic import A_star
            from Robot import robot


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
                def _next_position(position, goal):
                    row, column = position
                    goal_row, goal_column = goal
                    if row != goal_row:
                        row += 1 if goal_row > row else -1
                    elif column != goal_column:
                        column += 1 if goal_column > column else -1
                    return row, column

                def run(self):
                    """Generate timestamps until every robot reaches its goal."""
                    self.history.append(self._snapshot())
                    while any(new_robot.position != new_robot.goal for new_robot in self.robots):
                        for new_robot in self.robots:
                            if new_robot.position != new_robot.goal:
                                new_robot.position = self._next_position(
                                    new_robot.position, new_robot.goal
                                )
                        self.history.append(self._snapshot())

                def timestamp(self, index):
                    return self.history[index]


            def draw_shape(ax, row, column, robot_type, grid_size):
                """Draw the robot marker using the same row orientation as the grid."""
                center_x = column + 0.5
                center_y = grid_size - row - 0.5
                if robot_type == "driver":
                    ax.add_patch(Circle((center_x, center_y), 0.15, color="steelblue"))
                elif robot_type == "drone":
                    ax.add_patch(Rectangle((center_x - 0.15, center_y - 0.15), 0.3, 0.3, color="tomato"))
                elif robot_type == "humanoid":
                    points = [
                        (center_x, center_y + 0.15),
                        (center_x - 0.15, center_y - 0.15),
                        (center_x + 0.15, center_y - 0.15),
                    ]
                    ax.add_patch(Polygon(points, color="seagreen"))


            def draw_grid(ax, grid_size):
                for coordinate in range(grid_size + 1):
                    ax.plot([0, grid_size], [coordinate, coordinate], color="lightgray", linewidth=0.8)
                    ax.plot([coordinate, coordinate], [0, grid_size], color="lightgray", linewidth=0.8)


            def plan_path(start, goal, grid_size):
                """Return a valid path, accounting for the A* implementation's edge cells."""
                path = A_star(grid_size, start, goal)
                if not path or path[0] != start:
                    path.insert(0, start)
                return path


            def create_grid(grid_size, robot_count):
                grid = Grid(grid_size)
                for index in range(robot_count):
                    new_robot = robot.make_Robot(f"Robot {index + 1}", grid_size)
                    grid.add_robot(new_robot)
                    print(
                        f"{new_robot.name}: Type={type(new_robot).__name__}, "
                        f"Position={new_robot.position}, Goal={new_robot.goal}, "
                        f"Distance={new_robot.distance:.2f}"
                    )
                grid.run()
                paths = [
                    plan_path(new_robot.position, new_robot.goal, grid_size)
                    for new_robot in grid.robots
                ]
                return grid, paths


            def plot_grid_and_paths(grid, paths):
                """Open synchronized timestamp and planned-path windows."""
                colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]
                timestamp_figure, timestamp_axis = plt.subplots(figsize=(6, 6))
                path_figure, path_axis = plt.subplots(figsize=(6, 6))
                current_timestamp = 0

                def draw_timestamp(timestamp):
                    timestamp_axis.clear()
                    timestamp_axis.set_xlim(0, grid.columns)
                    timestamp_axis.set_ylim(0, grid.rows)
                    timestamp_axis.set_xticks(range(grid.columns + 1))
                    timestamp_axis.set_yticks(range(grid.rows + 1))
                    timestamp_axis.grid(True)
                    timestamp_axis.set_aspect("equal")
                    timestamp_axis.set_title(f"Robot timestamps: {timestamp + 1} of {len(grid.history)}")

                    for state in grid.timestamp(timestamp):
                        row, column = state["position"]
                        goal_row, goal_column = state["goal"]
                        timestamp_axis.plot(
                            [column + 0.5, goal_column + 0.5],
                            [grid.rows - row - 0.5, grid.rows - goal_row - 0.5],
                            color="gray",
                            linestyle="--",
                            linewidth=1.5,
                            zorder=1,
                        )
                        draw_shape(timestamp_axis, row, column, state["type"], grid.rows)
                    timestamp_figure.canvas.draw_idle()

                def draw_paths():
                    path_axis.clear()
                    draw_grid(path_axis, grid.columns)
                    for index, path in enumerate(paths):
                        color = colors[index % len(colors)]
                        path_axis.plot(
                            [column + 0.5 for row, column in path],
                            [grid.rows - row - 0.5 for row, column in path],
                            color=color,
                            linewidth=2,
                            marker="o",
                            label=grid.robots[index].name,
                        )
                        start_row, start_column = path[0]
                        goal_row, goal_column = path[-1]
                        path_axis.plot(start_column + 0.5, grid.rows - start_row - 0.5, "s", color=color)
                        path_axis.plot(
                            goal_column + 0.5,
                            grid.rows - goal_row - 0.5,
                            "s",
                            color=color,
                            fillstyle="none",
                            markeredgewidth=2,
                        )
                    path_axis.set_xlim(0, grid.columns)
                    path_axis.set_ylim(0, grid.rows)
                    path_axis.set_aspect("equal")
                    path_axis.set_xticks(range(grid.columns + 1))
                    path_axis.set_yticks(range(grid.rows + 1))
                    path_axis.set_title("Planned path per robot")
                    path_axis.set_xlabel("Column")
                    path_axis.set_ylabel("Row")
                    path_axis.legend(loc="upper right")
                    path_figure.canvas.draw_idle()

                def update(event):
                    nonlocal current_timestamp
                    if event.key in ("right", " "):
                        current_timestamp = min(current_timestamp + 1, len(grid.history) - 1)
                    elif event.key == "left":
                        current_timestamp = max(current_timestamp - 1, 0)
                    else:
                        return
                    draw_timestamp(current_timestamp)

                draw_timestamp(current_timestamp)
                draw_paths()
                timestamp_figure.canvas.mpl_connect("key_press_event", update)
                path_figure.canvas.mpl_connect("key_press_event", update)
                plt.show()


            def main():
                grid, paths = create_grid(grid_size=10, robot_count=10)
                plot_grid_and_paths(grid, paths)


            if __name__ == "__main__":
                main()
