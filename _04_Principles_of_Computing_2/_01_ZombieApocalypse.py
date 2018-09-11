# -*- encoding: utf-8 -*-
""" Zombie Apocalypse mini-project. Place obstacles, zombies and humans on the canvas and start simulation """
# use following link to test the program in 'codeskulptor': http://www.codeskulptor.org/#user45_VSFDSMacI4_12.py

import poc_grid
import poc_queue
import poc_zombie_gui


# global constants
EMPTY = 0  # Passable cells in the grid correspond to EMPTY cells while FULL cells are impassable
FULL = 1  # Humans and zombies can only inhabit passable cells of the grid. However, several humans and zombies may inhabit the same grid cell.
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """ Class for simulating zombie pursuit of human on grid with obstacles. This class is a sub-class of the Grid class and inherits the Grid class methods """
    def __init__(self, grid_height, grid_width, obstacle_list=None, zombie_list=None, human_list=None):  # initializer also takes three optional arguments which are lists of cells that initially contain obstacles, zombies and humans, respectively.
        """ Create a simulation of given size with given obstacles, humans, and zombies """
        poc_grid.Grid.__init__(self, grid_height, grid_width)  # here we call the SUPERCLASS CONSTRUCTOR

        if obstacle_list != None:  # if you choose to have obstacles, then we set those cells as 'FULL' (all other cells are to be 'EMPTY') if there aren't any we don't create a list
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:  # if there are any zombies or people we simply make a copy of that list and then we use it
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def clear(self):
        """ Set cells in obstacle grid to be empty. Reset zombie and human lists to be empty """
        poc_grid.Grid.clear(self)  # thanks to the INHERITANCE, we can just clear the grid via 'Grid'
        self._zombie_list = []
        self._human_list = []

    def add_zombie(self, row, col):
        """ Add zombie to the zombie list """
        self._zombie_list.append(tuple([row, col]))

    def num_zombies(self):
        """ Return number of zombies """
        return len(self._zombie_list)

    def zombies(self):
        """ Generator that yields the zombies in the order they were added. """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """ Add human to the human list """
        self._human_list.append(tuple([row, col]))

    def num_humans(self):
        """ Return number of humans """
        return len(self._human_list)

    def humans(self):
        """ Generator that yields the humans in the order they were added. """
        for human in self._human_list:
            yield human

    def compute_distance_field(self, entity_type):
        """ Function computes and returns a 2D distance field. Distance at member of entity_list is zero. Shortest paths avoid obstacles and use four-way distances """
        distance_field = [[self._grid_height * self._grid_width for dummy_row in range(self._grid_width)] for dummy_col in range(self._grid_height)]  # we populate the resulting array with the max distances possible (w*h)
        visited = [[EMPTY for dummy_row in range(self._grid_width)] for dummy_col in range(self._grid_height)]  # this is where we are going to store the info about teh cells already visited
        boundary = poc_queue.Queue()

        if entity_type == ZOMBIE:
            for zombie in self._zombie_list:
                boundary.enqueue(zombie)
        elif entity_type == HUMAN:
            for human in self._human_list:
                boundary.enqueue(human)

        for cell in boundary:
            visited[cell[0]][cell[1]] = FULL
            distance_field[cell[0]][cell[1]] = 0

        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            current_value = distance_field[current_cell[0]][current_cell[1]]
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])  # we are going to process the neighbours of a particular cell one at the time and increase the distance by 1 for each neighbouring ring

            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]) and visited[neighbor[0]][neighbor[1]] == EMPTY:  # if the grid cell is empty (no obstacles) and is not yet visited (a similar object is already closer)
                    visited[neighbor[0]][neighbor[1]] = FULL
                    boundary.enqueue(neighbor)  # now the neighbor becomes a center for the neighboring cells
                    distance_field[neighbor[0]][neighbor[1]] = current_value + 1  # for all the neighbours we increase the value of the cell by 1

        return distance_field

    def move_humans(self, zombie_distance_field):
        """ Function that moves humans away from zombies, diagonal moves are allowed """
        for index in range(len(self._human_list)):  # we have to use the indexes here as we will have to update the very human in the end
            best_pos = self._human_list[index]  # we assign the best position and value so far to the current human position (in case we are surrounded for example)
            best_dis = zombie_distance_field[best_pos[0]][best_pos[1]]
            neighbours = self.eight_neighbors(best_pos[0], best_pos[1])  # humans can make diagonal moves, so we pick all 8 neighbors

            for neighbour in neighbours:
                neigh_dis = zombie_distance_field[neighbour[0]][neighbour[1]]
                if neigh_dis > best_dis and self.is_empty(neighbour[0], neighbour[1]):  # here we just analyze each neighbor's distance one by one in order to find the place furthest away from the zombie
                    best_dis = neigh_dis
                    best_pos = neighbour
            self._human_list[index] = best_pos  # here we just update the 'human_list' and we don't return anything from this function

    def move_zombies(self, human_distance_field):
        """ Function that moves zombies towards humans, no diagonal moves are allowed """
        for index in range(len(self._zombie_list)):  # we have to use the indexes here as we will have to update the very zombie in the end
            best_pos = self._zombie_list[index]  # we assign the best position and value so far to the current zombie position
            best_dis = human_distance_field[best_pos[0]][best_pos[1]]
            neighbours = self.four_neighbors(best_pos[0], best_pos[1])  # zombies can not make diagonal moves, so we pick all 4 neighbors

            for neighbour in neighbours:
                neigh_dis = human_distance_field[neighbour[0]][neighbour[1]]
                if neigh_dis < best_dis and self.is_empty(neighbour[0], neighbour[1]):  # here we just analyze each neighbor's distance one by one in order to find the place the closest to humans as possible
                    best_dis = neigh_dis
                    best_pos = neighbour
            self._zombie_list[index] = best_pos  # here we just update the 'zombie_list' and we don't return anything from this function


# Start up gui for simulation - You will need to write some code above before this will work without errors
poc_zombie_gui.run_gui(Apocalypse(30, 40))
