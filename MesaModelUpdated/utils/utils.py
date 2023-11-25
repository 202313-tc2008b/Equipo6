import networkx as nx
import heapq
from .map import grid_size, RoadIntersections

def calculate_steps_between_points(start_point, end_point):
    x_diff = end_point[0] - start_point[0]
    y_diff = end_point[1] - start_point[1]

    steps_x = abs(x_diff)
    steps_y = abs(y_diff)

    step_increment_x = x_diff // steps_x if steps_x else 0
    step_increment_y = y_diff // steps_y if steps_y else 0

    steps = []
    current = start_point
    for _ in range(max(steps_x, steps_y)):
        x = current[0] + step_increment_x
        y = current[1] + step_increment_y
        current = (x, y)
        steps.append(current)

    return steps

def calculate_manhattan_distance(point1, point2):
    return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])

def generate_graph(intersection_points):
    network = nx.DiGraph()
    for node, neighbors in intersection_points.items():
        for adjacent, weight in neighbors.items():
            network.add_edge(node, adjacent, cost=weight)
    return network

def execute_astar_algorithm(network, start, end, distance_heuristic):
    priority_queue = [(0, start)]
    heapq.heapify(priority_queue)
    origin = {}
    total_cost = {start: 0}

    while priority_queue:
        current_cost, current_node = heapq.heappop(priority_queue)

        if current_node == end:
            break

        for next_node in network.neighbors(current_node):
            new_cost = total_cost[current_node] + network[current_node][next_node]['cost']
            if next_node not in total_cost or new_cost < total_cost[next_node]:
                total_cost[next_node] = new_cost
                priority = new_cost + distance_heuristic(end, next_node)
                heapq.heappush(priority_queue, (priority, next_node))
                origin[next_node] = current_node

    path = []
    current = end
    while current != start:
        path.append(current)
        current = origin[current]
    path.append(start)
    path.reverse()

    detailed_path = []
    for i in range(len(path) - 1):
        detailed_path.extend(calculate_steps_between_points(path[i], path[i + 1]))

    return detailed_path

def render_path_on_grid(path, size_of_grid):
    grid_representation = [['.' for _ in range(size_of_grid[1])] for _ in range(size_of_grid[0])]

    for point in path:
        x_adjusted = size_of_grid[0] - 1 - point[1]
        y_adjusted = point[0]
        grid_representation[x_adjusted][y_adjusted] = '*'

    for row in grid_representation:
        print(' '.join(row))
