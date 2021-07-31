import pygame
import math
from queue import PriorityQueue

from pygame.constants import CONTROLLER_AXIS_LEFTX, KEYDOWN
from Node import Node


size = 1000
rows = 50
WINDOW = pygame.display.set_mode((size, size))


def make_grid(size, rows) -> list[Node]:
    grid = []

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            grid[i].append(Node(i, j, size//rows, rows))

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, Node.BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, Node.BLACK, (j * gap, 0), (j * gap, width))


def draw_nodes(window, grid, rows, size):
    for row in grid:
        for node in row:
            node.draw_node(window)
    draw_grid(WINDOW, rows, size)
    pygame.display.update()


def get_grid_pos(rows, size, pos):
    node_size = size // rows
    x, y = pos
    return (x // node_size, y // node_size)


def handle_wall(pos, grid):
    x, y = pos
    # y is rows because of structure of 2d array
    node = grid[y][x]
    node.make_wall()


def a_star(grid, start, end, window, rows, size):
    open = PriorityQueue()

    while not open.empty():
        # handle close event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        draw_nodes(window, grid, rows, size)


def main(window, size, rows):
    grid = make_grid(size, rows)
    draw_nodes(window, grid, rows, size)

    # start and end nodes declared
    start = None
    end = None

    run = True
    while run:
        # go through ever event in list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # rightclick
            if pygame.mouse.get_pressed()[2]:
                pos = get_grid_pos(rows, size, pygame.mouse.get_pos())
                x, y = pos
                node = grid[y][x]
                if node == start:
                    start = None
                if node == end:
                    end = None

                node.reset_node()
                draw_nodes(window, grid, rows, size)
            elif pygame.mouse.get_pressed()[0]:  # left click
                pos = get_grid_pos(rows, size, pygame.mouse.get_pos())
                x, y = pos
                node = grid[y][x]

                if not start:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = grid[y][x]
                    end.make_end()
                elif node != start and node != end:
                    handle_wall(pos, grid)
                draw_nodes(window, grid, rows, size)
            elif event.type == pygame.KEYDOWN:  # any key pressed
                print("adadad")
                a_star(grid, start, end, window, rows, size)
        draw_nodes(window, grid, rows, size)
    pygame.quit()


main(WINDOW, size, rows)
