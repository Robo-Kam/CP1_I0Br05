"""A visual 5x5 grid for storing object positions and timestamp history."""

#Grid Class for creating a grid, displaying robot position, goal, progress, and current timestamp



#initialize grid as class

#Create 10 different robots of different types with initial positions

#function for adding robot to grid

#func for robot path planning

#func for moving robot to new position

#func for saving robot position on grid from timestamp

#function for removing robot from grid

#func for giving robot a symbol and line from current position to origin

#Robot func for switching between time stamps press 2 keys for forward or backward

#Robot func for printing viewable display




class Grid:
    """Store objects by position and render them as a text grid."""

    def __init__(self, rows=5, columns=5):
        if rows != 5 or columns != 5:
            raise ValueError("Grid must be 5x5")

        self.rows = rows
        self.columns = columns
        self.positions = {}
        self.history = []
        self._save_snapshot()

    def _save_snapshot(self):
        """Save a copy of the current positions as one timestamp."""
        self.history.append(dict(self.positions))

    def _validate_position(self, row, column):
        if not (0 <= row < self.rows and 0 <= column < self.columns):
            raise ValueError("Position must be inside the 5x5 grid")

    def add_object(self, obj, row, column, symbol=None):
        """Place an object on the grid and return its display symbol."""
        self._validate_position(row, column)
        if obj in self.positions:
            raise ValueError("Object is already on the grid")

        if any(position[:2] == (row, column) for position in self.positions.values()):
            raise ValueError("Grid position is already occupied")

        display_symbol = symbol or getattr(obj, "symbol", None) or str(obj)[0]
        if len(display_symbol) != 1:
            raise ValueError("symbol must be exactly one character")
        self.positions[obj] = (row, column, display_symbol)
        self._save_snapshot()
        return display_symbol

    def move_object(self, obj, row, column):
        """Move an existing object to a new unoccupied position."""
        self._validate_position(row, column)
        if obj not in self.positions:
            raise KeyError("Object is not on the grid")

        if any(
            other_position[:2] == (row, column)
            for other_obj, other_position in self.positions.items()
            if other_obj != obj
        ):
            raise ValueError("Grid position is already occupied")

        _, _, symbol = self.positions[obj]
        self.positions[obj] = (row, column, symbol)
        self._save_snapshot()

    def remove_object(self, obj):
        """Remove an object from the grid."""
        del self.positions[obj]
        self._save_snapshot()

    def get_position(self, obj):
        """Return an object's ``(row, column)`` position."""
        row, column, _ = self.positions[obj]
        return row, column

    def render(self):
        """Return the current grid as a printable string."""
        cells = [["." for _ in range(self.columns)] for _ in range(self.rows)]
        for row, column, symbol in self.positions.values():
            cells[row][column] = symbol
        return "\n".join(" ".join(row) for row in cells)

    def display(self):
        """Print the current grid."""
        print(self.render())

    def __str__(self):
        return self.render()

    def plot(self, num_timestamps=None):
        """Display timestamped grid snapshots with keyboard navigation.

        Use the left/right arrow keys, ``A``/``D``, or keypad ``4``/``6``
        to move through the selected timestamps. ``num_timestamps`` limits
        the display to the most recent snapshots.
        """
        if num_timestamps is None:
            snapshots = self.history
        else:
            if not isinstance(num_timestamps, int) or num_timestamps < 1:
                raise ValueError("num_timestamps must be a positive integer")
            snapshots = self.history[-num_timestamps:]

        if not snapshots:
            raise ValueError("There are no timestamps to display")

        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        timestamp_index = 0

        def draw_snapshot():
            ax.clear()
            ax.set_xlim(0, self.columns)
            ax.set_ylim(0, self.rows)
            ax.set_xticks(range(self.columns + 1))
            ax.set_yticks(range(self.rows + 1))
            ax.grid(True)

            for row, column, symbol in snapshots[timestamp_index].values():
                ax.text(
                    column + 0.5,
                    self.rows - row - 0.5,
                    symbol,
                    ha="center",
                    va="center",
                    fontsize=20,
                )

            ax.set_title(
                f"Timestamp {timestamp_index + 1} of {len(snapshots)} "
                "(left/right or keypad 4/6)"
            )
            ax.set_aspect("equal")
            fig.canvas.draw_idle()

        def on_key(event):
            nonlocal timestamp_index
            if event.key in ("left", "a", "4"):
                timestamp_index = max(0, timestamp_index - 1)
            elif event.key in ("right", "d", "6"):
                timestamp_index = min(len(snapshots) - 1, timestamp_index + 1)
            else:
                return
            draw_snapshot()

        fig.canvas.mpl_connect("key_press_event", on_key)
        draw_snapshot()
        plt.show()