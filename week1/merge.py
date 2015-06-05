"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
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
