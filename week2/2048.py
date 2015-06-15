"""
Clone of 2048 game.
"""

#import poc_2048_gui
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
    # replace with your code
    tmp_line = [0] * len(line)
    result_line = [0] * len(line)
    point_i = 0
    point_j = 0
    # copy line to tmp_line, move 0 to the end
    while point_i < len(line):
        if line[point_i] != 0:
            tmp_line[point_j] = line[point_i]
            point_j += 1
        point_i += 1
    # merge (from tmp_line to line)
    point_i = 0
    point_j = 0
    while point_i < len(line):
        if point_i == len(line) - 1:
            result_line[point_j] = tmp_line[point_i]
            break
        if tmp_line[point_i] == tmp_line[point_i+1]:
            result_line[point_j] = tmp_line[point_i] * 2
            point_j += 1
            point_i += 2
        else:
            result_line[point_j] = tmp_line[point_i]
            point_i += 1
            point_j += 1
    return result_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._height = grid_height
        self._width = grid_width
        self._grid = list()
        # pre compute initial indices for four directions, store in dictionary
        self._initial_indices = {}
        self._initial_indices[UP] = [(0,col) for col in range(self._width)]
        self._initial_indices[DOWN] = [(self._height-1,col) for col in range(self._width)]
        self._initial_indices[LEFT] = [(row,0) for row in range(self._height)]
        self._initial_indices[RIGHT] = [(row, self._width-1) for row in range(self._height)]
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        for dummy_row in range(self._height):
            self._grid.append([0] * self._width)
        self.new_tile()
        #self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return '\n'.join([' '.join(['%4d' % tmp_col for tmp_col in tmp_row]) for tmp_row in self._grid])

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        cell_change_flag = False
        for initial_cell in self._initial_indices[direction]:
            cell_array = list()
            if direction == UP or direction == DOWN:
                len_array = self._height
            else:
                len_array = self._width
            for tmp_i in range(len_array):
                # get the array of cells (x,y)
                cell_array.append((initial_cell[0] + tmp_i * OFFSETS[direction][0], initial_cell[1] + tmp_i * OFFSETS[direction][1]))
            # get that line of numbers
            num_array = [self._grid[row][col] for (row, col) in cell_array]
            # merge
            merged_array = merge(num_array)
            # update the grid and check if there is any change
            for tmp_i in range(len(cell_array)):
                row = cell_array[tmp_i][0]
                col = cell_array[tmp_i][1]
                if self._grid[row][col] != merged_array[tmp_i]:
                    cell_change_flag = True
                    self._grid[row][col] = merged_array[tmp_i]
        if cell_change_flag:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        tmp_row = None
        tmp_col = None
        tmp_random = 1.0
        tmp_value = 2
        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == 0:
                    new_random = random.random()
                    if new_random < tmp_random:
                        tmp_row = row
                        tmp_col = col
                        tmp_random = new_random
        if tmp_row is not None and tmp_col is not None:
            if random.random() < 0.1:
                tmp_value = 4
        self.set_tile(tmp_row, tmp_col, tmp_value)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._grid[row][col]

#poc_2048_gui.run_gui(TwentyFortyEight(2, 2))

