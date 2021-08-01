# class for node in pathfinding algorithm
import pygame


class Node:
    RED = (226, 71, 71)
    GREEN = (117, 255, 74)
    BLUE = (0, 133, 255)
    YELLOW = (255, 255, 80)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    GREY = (128, 128, 128)
    TURQUOISE = (64, 224, 208)

    def __init__(self, row, col, size, num_rows):
        self.row = row
        self.col = col
        self.x = col * size
        self.y = row * size
        self.size = size
        self.num_rows = num_rows
        self.neighbors = []
        self.color = self.WHITE

    def get_position(self):
        return self.row, self.col

    def get_neighbors(self):
        return self.neighbors

    def reset_node(self):
        self.color = self.WHITE  # makes node white again

    def is_open(self):
        return self.color == self.GREEN  # checj if color is green ie visitable node

    def make_open(self):
        self.color = self.GREEN  # make green

    def is_closed(self):
        return self.color == self.BLUE

    def make_closed(self):
        self.color = self.BLUE

    def is_start(self):
        return self.color == self.ORANGE

    def make_start(self):
        self.color = self.ORANGE

    def is_wall(self):
        return self.color == self.BLACK

    def make_wall(self):
        self.color = self.BLACK

    def is_end(self):
        return self.color == self.PURPLE

    def make_end(self):
        self.color = self.PURPLE

    def make_path(self):
        self.color = self.YELLOW

    def draw_node(self, window):
        pygame.draw.rect(window, self.color,
                         (self.x, self.y, self.size, self.size))

    def update_neighbors(self, grid):
        self.neighbors = []
        # add bottom nbeighor
        if self.row < self.num_rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])

        # add top neighbor
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])

        # add left neighbor
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])

        # add right neighbor
        if self.col < self.num_rows - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])

        # add bottom right niehgbor
        if (self.col < self.num_rows - 1 and self.row < self.num_rows - 1
                and not grid[self.row + 1][self.col + 1].is_wall()):
            self.neighbors.append(grid[self.row + 1][self.col + 1])

        # add bottom left neighbor
        if(self.col > 0 and self.row < self.num_rows - 1
                and not grid[self.row + 1][self.col - 1].is_wall()):
            self.neighbors.append(grid[self.row + 1][self.col - 1])

        # add top right neighbor
        if (self.col < self.num_rows - 1 and self.row > 0
                and not grid[self.row - 1][self.col + 1].is_wall()):
            self.neighbors.append(grid[self.row - 1][self.col + 1])

        # add top left neighbor
        if(self.col > 0 and self.row > 0
                and not grid[self.row - 1][self.col - 1].is_wall()):
            self.neighbors.append(grid[self.row - 1][self.col - 1])

    # func for priority queue to compare nodes
    def __lt__(self, other):
        return False
