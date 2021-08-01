import pygame
import math
from queue import PriorityQueue
from Node import Node


size = 1000
rows = 50
WINDOW = pygame.display.set_mode((size, size))
pygame.display.set_caption("A* Search Algorithm")


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


def reconstruct_path(came_from, current, draw_nodes):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw_nodes()


def a_star(grid, start, end, draw_nodes):
    open = PriorityQueue()
    # put as tuples, holding f_score and node
    open.put((0, start))

    # set of nodes in open to test for membership
    open_hash_set = {start}

    # map to hold previous nodes
    came_from = {}

    # map to hold g_scores, default to infinityfor all nodes except for start at 0
    g_scores = {node: float("inf") for row in grid for node in row}
    g_scores[start] = 0

    # map to hold f_scores, default to infinity for all nodes except for start at h()
    f_scores = {node: float("inf") for row in grid for node in row}
    f_scores[start] = euclidean_dist(start, end)

    while not open.empty():
        # handle close event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # get node from priorirty queue with lowers f score, and remove from set
        current = open.get()[1]
        open_hash_set.remove(current)

        # if we have reached  end, we are done
        if end == current:
            reconstruct_path(came_from, current, draw_nodes)
            end.make_end()
            start.make_start()
            return True

        # go through each neighbor
        for neighbor in current.get_neighbors():
            # get g_score of curr node
            temp_g_score = g_scores[current] + \
                euclidean_dist(current, neighbor)

            # if neighbor is further from start
            if temp_g_score < g_scores[neighbor]:
                # this path is better than before, save to came_from and scores lists
                came_from[neighbor] = current
                g_scores[neighbor] = temp_g_score
                f_scores[neighbor] = temp_g_score + \
                    euclidean_dist(neighbor, end)
                # add neigjbor and f_score to open set
                if neighbor not in open_hash_set:
                    open.put((f_scores[neighbor], neighbor))
                    open_hash_set.add(neighbor)
                    neighbor.make_open()

        # close node fter done, if not start
        if current != start:
            current.make_closed()
        draw_nodes()

    return False


def euclidean_dist(node1, node2):
    x1, y1 = node1.get_position()
    x2, y2 = node2.get_position()

    return math.sqrt(abs(x2 - x1) + abs(y2 - y1))


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

                if event.key == pygame.K_SPACE and start and end:

                    # update all neighbors
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    a_star(grid, start, end, lambda: draw_nodes(
                        window, grid, rows, size))

                # if any key but space is clicked, restart board
                else:
                    start = None
                    end = None
                    grid = make_grid(size, rows)
        draw_nodes(window, grid, rows, size)
    pygame.quit()


if __name__ == "__main__":
    main(WINDOW, size, rows)
