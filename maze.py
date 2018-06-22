#!/usr/bin/python3

from PIL import Image
import dijkstra as d
from math import inf as infinity
import argparse

# Black
COLOR_WALL = (0, 0, 0)
# White
COLOR_PATH = (255, 255, 255)

# Red
COLOR_START = (255, 0, 0)
# Green
COLOR_END = (0, 255, 0)
# Blue
COLOR_SOLVED = (0, 0, 255)

parser = argparse.ArgumentParser(description="Solve input PNG maze file")
parser.add_argument("-i", "--input", help="Maze file. Defaults to maze.png",
                    default="maze.png", required=False)
parser.add_argument("-o", "--output", default="solved.png",
                    help="PNG file to output to. Defaults to solved.png")

args = parser.parse_args()

try:
    image = Image.open(args.input)
    pixels = image.load()
except:
    print("Could not load file", args.input)
    exit()

nodes = [[None for _ in range(image.width)] for __ in range(image.height)]

for x in range(image.width):
    for y in range(image.height):
        pixel = pixels[x, y]
        if pixel == COLOR_WALL:
            nodes[y][x] = None
        else:
            nodes[y][x] = d.Node(x, y)

        if pixel == COLOR_START:
            initial_coords = (x, y)
        if pixel == COLOR_END:
            destination_coords = (x, y)

graph = d.Graph(nodes, initial_coords, destination_coords)

destination_distance = d.dijkstra(graph)

initial_node = graph.graph[initial_coords[1]][initial_coords[0]]
destination_node = graph.graph[destination_coords[1]][destination_coords[0]]

nodes = graph.get_nodes()

for node in nodes:
    if node:
        node.visited = False

current_node = destination_node
smallest_tentative_distance = destination_distance
# Go from destination node to initial node to find path
while current_node is not initial_node:
    neighbors = graph.get_neighbors(current_node)
    for neighbor in neighbors:
        if not neighbor or neighbor.visited:
            continue
        if neighbor.tentative_distance < smallest_tentative_distance:
            smallest_tentative_distance = neighbor.tentative_distance
            neighbor.visited = True
            current_node = neighbor
    pixels[current_node.x, current_node.y] = COLOR_SOLVED


image.save(args.output, "PNG")
