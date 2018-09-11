# -*- encoding: utf-8 -*-
""" An example of creating a distance field using Manhattan distance """

GRID_HEIGHT = 6
GRID_WIDTH = 8


def manhattan_distance(row0, col0, row1, col1):
    """ Compute the Manhattan distance between the cells (row0, col0) and (row1, col1) """
    return abs(row0 - row1) + abs(col0 - col1)  # the Manhattan Distance between two points (x0,y0) and (x1,y1) is: |x0−x1| + |y0−y1|


def create_distance_field(entity_list):
    """ Create a Manhattan distance field that contains the minimum distance to each entity (zombies or humans) in entity_list. Each entity is represented as a grid position of the form (row, col) """
    distance_field = [[GRID_HEIGHT + GRID_WIDTH for dummy_row in range(GRID_WIDTH)] for dummy_col in range(GRID_HEIGHT)]  # first we fill-in the all the fields in the matrix with the biggest distance possible
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):  # for each cell in our grid we are coing to calculate distances to both cells
            distance = min([manhattan_distance(entity[0], entity[1], row, col) for entity in entity_list])  # here we calculate the distances from the CURRENT CELL to both TARGET CELLS and pick the smallest
            # distance = [manhattan_distance(entity[0], entity[1], row, col) for entity in entity_list]  # this is without picking the minimal value, so we can see both distances
            distance_field[row][col] = distance
    return distance_field


def print_field(field):
    """ Print a distance field in a human readable manner with one row per line """
    for grid_row in range(GRID_HEIGHT):
        print(field[grid_row])


def run_example():
    """ Create and print a small distance field """
    field = create_distance_field([[4, 0], [2, 5]])
    print_field(field)


run_example()


# Sample output for the default example
# [4, 5, 5, 4, 3, 2, 3, 4]
# [3, 4, 4, 3, 2, 1, 2, 3]
# [2, 3, 3, 2, 1, 0, 1, 2]  # cells that contain an entity should always have a distance of zero (4, 0)
# [1, 2, 3, 3, 2, 1, 2, 3]
# [0, 1, 2, 3, 3, 2, 3, 4]  # cells that contain an entity should always have a distance of zero (2, 5)
# [1, 2, 3, 4, 4, 3, 4, 5]
