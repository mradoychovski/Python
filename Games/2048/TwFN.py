"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    last = 0
    index = 0
    merged = True
    result = [0 for dummy_i in range(len(line))]
    for item in line:
        if item != 0:
            if merged:
                last = item
                merged = False
            else:
                if last == item:
                    result[index] = 2 * last
                    last = 0
                    merged = True
                else:
                    result[index] = last
                    last = item
                index += 1

    result[index] = last
    return result


class TwentyFortyEight(object):
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.grid_h = grid_height
        self.grid_w = grid_width
        self.grid = [[0 for dummy_col in range(self.grid_w)]
            for dummy_row in range(self.grid_h)]
        self.init_tiles = {
            1: [(0, u) for u in range(self.grid_w)],
            2: [(self.grid_h-1, d) for d in range(self.grid_w)],
            3: [(l, 0) for l in range(self.grid_h)],
            4: [(r, self.grid_w-1) for r in range(self.grid_h)]}

    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.grid = \
            [[0 for dummy_col in range(self.grid_w)]
                for dummy_row in range(self.grid_h)]

    def __str__(self):
        """
        Return  a string representation of the grid for debugging.
        """
        grid_repr = ''
        for row in range(self.grid_h):
            grid_repr += ' '.join(str(col) for col in self.grid[row]) + '\n'
        return grid_repr

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_h

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_w

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        def navigation(grid_dir):
            """
            Helper function
            """
            for tile in self.init_tiles[direction]:
                tmp = []
                for nav in range(grid_dir):
                    row = tile[0] + OFFSETS[direction][0] * nav
                    col = tile[1] + OFFSETS[direction][1] * nav
                    tmp.append(self.grid[row][col])
                merge_tmp = merge(tmp)
                for nav in range(grid_dir):
                    row = tile[0]+OFFSETS[direction][0]*nav
                    col = tile[1]+OFFSETS[direction][1]*nav
                    self.grid[row][col] = merge_tmp[nav]

        if direction <= 2:
            navigation(self.grid_h)
        else:
            navigation(self.grid_w)
        self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        empty = []
        for row in range(self.grid_h):
            for col in range(self.grid_w):
                if self.grid[row][col] == 0:
                    empty.append((row, col))
        if empty != []:
            choice = random.randint(1, 10)
            square = random.choice(empty)
            if choice < 10:
                self.set_tile(square[0], square[1], 2)
            else:
                self.set_tile(square[0], square[1], 4)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
