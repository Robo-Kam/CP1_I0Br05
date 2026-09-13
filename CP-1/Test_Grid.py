
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle


# Add one list of shapes for each update.
# Each shape is: (row, column, shape)

goals=[

		(1, 4, "circle"),
		(2, 4, "square"),
		(3, 4, "triangle"),
	


]

updates = [
	[
		(0, 1, "circle"),
		(2, 3, "square"),
		(4, 4, "triangle"),
	],
	[
		(0, 2, "circle"),
		(2, 2, "square"),
		(3, 4, "triangle"),
	],
	[
		(1, 2, "circle"),
		(1, 3, "square"),
		(2, 4, "triangle"),
	],
]


def draw_shape(ax, row, column, shape):
	center_x = column + 0.5
	center_y = 4 - row + 0.5

	if shape == "circle":
		ax.add_patch(Circle((center_x, center_y), 0.1, color="steelblue"))
	elif shape == "square":
		ax.add_patch(Rectangle((center_x - 0.1, center_y - 0.1),
							   0.15, 0.15, color="tomato"))
	elif shape == "triangle":
		points = [
			(center_x, center_y + 0.1),
			(center_x - 0.1, center_y - 0.1),
			(center_x + 0.1, center_y - 0.1),
		]
		ax.add_patch(Polygon(points, color="seagreen"))
	else:
		raise ValueError(f"Unknown shape: {shape}")

	return center_x, center_y

fig, ax = plt.subplots()

def draw_update(update_number):
	"""Draws the grid and shapes for a specific update number."""
	ax.clear()
	ax.set_xlim(0, 5)
	ax.set_ylim(0, 5)
	ax.set_xticks(range(6))
	ax.set_yticks(range(6))
	ax.grid(True)
	ax.set_aspect("equal")
	ax.set_title(f"Timestamp {update_number + 1} of {len(updates)}")

	if update_number < len(updates):
		current_shapes = updates[update_number]

		for current, goal in zip(current_shapes, goals):
			current_row, current_column, _ = current
			goal_row, goal_column, _ = goal
			goal_x, goal_y = goal_column + 0.5, 4 - goal_row + 0.5
			current_x, current_y = current_column + 0.5, 4 - current_row + 0.5
			ax.plot(
				[current_x,goal_x],
				[current_y,goal_y],
				color="gray",
				linestyle="--",
				linewidth=1.5,
				zorder=1,
			)

	for row, column, shape in updates[update_number]:
		draw_shape(ax, row, column, shape)
		draw_shape(ax, row, column, shape)

	fig.canvas.draw_idle()


current_update = 0
draw_update(current_update)


def toggle_update(event):
	"""Uses Key Inputs to toggle between updates"""
    
	global current_update

	if event.key in ("right", " "):
		current_update = (current_update + 1) % len(updates)
	elif event.key == "left":
		current_update = (current_update - 1) % len(updates)
	else:
		return

	draw_update(current_update)


fig.canvas.mpl_connect("key_press_event", toggle_update)

plt.show()



