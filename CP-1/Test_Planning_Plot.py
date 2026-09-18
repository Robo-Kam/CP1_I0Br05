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


# Example usage:
# robot_1_path = [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]
# robot_2_path = [(3, 3), (3, 4), (4, 4)]
# plot_robot_paths([robot_1_path, robot_2_path], grid_size=5)
griddie=10
robot_path1=A_star(griddie,(0,0),(5,5))
robot_path2=A_star(griddie,(0,2),(6,6))
print(robot_path1)


plot_robot_paths([robot_path1,robot_path2],grid_size=griddie)
