"""A visual 5x5 grid for storing object positions."""

#Grid Class for creating a grid, displaying robot position, goal, progress, and current timestamp



#initialize grid

#function for adding robot to grid

#func for moving robot to new position

#function for removing robot from grid







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

    def remove_object(self, obj):
        """Remove an object from the grid."""
        del self.positions[obj]

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

    import matplotlib.pyplot as plt

    def plot(self):
        fig, ax = plt.subplots()

        ax.set_xlim(0, 5)
        ax.set_ylim(0, 5)
        ax.set_xticks(range(6))
        ax.set_yticks(range(6))
        ax.grid(True)

        for obj, (row, column, symbol) in self.positions.items():
            ax.text(
                column + 0.5,
                4.5 - row,
                symbol,
                ha="center",
                va="center",
                fontsize=20,
            )

        ax.set_aspect("equal")
        plt.show()