import random
import math
import re

import numpy as np
import matplotlib.pyplot as plt
import heapq


class CityGrid:
    def __init__(self, n, m, percent_blocked_blocks, tower_price, budget):
        self.city_longitude = n
        self.city_width = m
        self.city_space = self.city_longitude * self.city_width
        self.blocked_blocks, self.grid = self.build_city_grid(percent_blocked_blocks)
        self.free_blocks = {index for index in range(0, self.city_space) if index not in self.blocked_blocks}
        self.tower_price = tower_price
        self.budget = budget
        self.towers = []
        self.towers_graph = {}

    def index_in_cords(self, index):
        return {"i_longitude": index // self.city_width, "i_width": index % self.city_width}

    def cords_in_index(self, i_longitude, i_width):
        return i_longitude * self.city_longitude + i_width

    def build_city_grid(self, percent_blocked_blocks):
        grid = [
            [{"is_locked": False, "in_covering": False, "install_tower": False,
              "index": self.cords_in_index(i_longitude, i_width), "belonging_towers": []}
             for i_width in range(0, self.city_width)]
            for i_longitude in range(0, self.city_longitude)
        ]
        len_blocked_blocks = math.ceil((self.city_space / 100) * percent_blocked_blocks)
        blocked_blocks = [index for index in random.sample(range(self.city_space), len_blocked_blocks)]
        for index in blocked_blocks:
            cords = self.index_in_cords(index)
            grid[cords["i_longitude"]][cords["i_width"]]["is_locked"] = True
            grid[cords["i_longitude"]][cords["i_width"]]["in_covering"] = True
        return blocked_blocks, grid

    def visual_example(self, example_num, paths=None):
        rows = len(self.grid)
        cols = len(self.grid[0])
        colors = np.zeros((rows + 2, cols + 2))
        value = np.zeros((rows + 2, cols + 2))
        for i in range(rows):
            for j in range(cols):
                value[i + 1][j + 1] = self.grid[i][j]['index']
                if self.grid[i][j]['is_locked']:
                    colors[i + 1][j + 1] = 10
                elif self.grid[i][j]['in_covering'] and self.grid[i][j]['install_tower']:
                    value[i + 1][j + 1] = -1
                    colors[i + 1][j + 1] = 4
                elif self.grid[i][j]['in_covering']:
                    colors[i + 1][j + 1] = 3
                else:
                    colors[i + 1][j + 1] = 0

        fig, ax = plt.subplots()
        ax.imshow(colors, cmap='YlGn')

        for i in range(rows):
            for j in range(cols):
                cell_value = colors[i + 1][j + 1]
                if int(value[i + 1][j + 1]) == -1:
                    ax.text(j + 1, i + 1, "♜", ha='center', va='center', fontsize=12)
                elif cell_value == 10:
                    ax.text(j + 1, i + 1, int(value[i + 1][j + 1]), ha='center', va='center', fontsize=12,
                            color='white')
                elif cell_value > 5 and self.grid[i][j]['in_covering'] and not self.grid[i][j]['install_tower']:
                    ax.text(j + 1, i + 1, int(value[i + 1][j + 1]), ha='center', va='center', fontsize=12, color='grey')
                else:
                    ax.text(j + 1, i + 1, int(value[i + 1][j + 1]), ha='center', va='center', fontsize=12,
                            color='black')

        if paths:
            for i in range(1, len(paths)):
                start_path = paths[i - 1]
                end_path = paths[i]
                x_start = start_path % cols + 1
                y_start = start_path // cols + 1
                x_end = end_path % cols + 1
                y_end = end_path // cols + 1
                ax.plot([x_start, x_end], [y_start, y_end], 'r-', linewidth=2)

        for i in range(rows + 2):
            for j in range(cols + 2):
                if i == 0 or i == rows + 1 or j == 0 or j == cols + 1:
                    if (j - 0.5 +  i - 0.5) % 2 != 0:
                        facecolor = "white"
                    else:
                        facecolor = "black"
                    rect = plt.Rectangle((j - 0.5, i - 0.5), 1, 1, linewidth=1, edgecolor='black', facecolor=facecolor)
                    ax.add_patch(rect)

        plt.title(f'Example {example_num}')
        if example_num > 1:
            gs = fig.add_gridspec(rows, cols + 2)
            ax_label1 = fig.add_subplot(gs[:, -1])
            ax_label1.text(0.5, 0.5, f"Бюджет = {self.budget}$\nЦена башни = {self.tower_price}$\nПотратили {len(self.towers_graph.keys()) * self.tower_price}$",
                           fontsize=12, fontweight='bold', ha='center', va='center')
            ax_label1.axis('off')
        plt.show()

    def update_graph(self, neighboring_tower, index):
        if neighboring_tower not in self.towers_graph[index]:
            self.towers_graph[index].append(neighboring_tower)
        if neighboring_tower not in self.towers_graph: self.towers_graph[neighboring_tower] = []
        if index not in self.towers_graph[neighboring_tower]:
            self.towers_graph[neighboring_tower].append(index)

    def install_tower(self, index, radius, free_square=None):
        tower_cords = self.index_in_cords(index)
        if self.grid[tower_cords["i_longitude"]][tower_cords["i_width"]]["is_locked"]:
            return False

        self.grid[tower_cords["i_longitude"]][tower_cords["i_width"]]["install_tower"] = True
        if index not in self.towers_graph: self.towers_graph[index] = []
        external_coverage_area = [self.cords_in_index(i_longitude, i_width) for i_width in
                                  range(tower_cords["i_width"] - radius - 1, tower_cords["i_width"] + radius + 1 + 1)
                                  for i_longitude in
                                  range(tower_cords["i_longitude"] - radius - 1,
                                        tower_cords["i_longitude"] + radius + 2)]
        for i_longitude in range(tower_cords["i_longitude"] - radius, tower_cords["i_longitude"] + radius + 1):
            for i_width in range(tower_cords["i_width"] - radius, tower_cords["i_width"] + radius + 1):
                external_coverage_area.remove(self.cords_in_index(i_longitude, i_width))
                if not 0 <= i_width < self.city_width \
                        or not 0 <= i_longitude < self.city_longitude: continue
                self.grid[i_longitude][i_width]["in_covering"] = True
                self.grid[i_longitude][i_width]["belonging_towers"].append(index)
                for neighboring_tower in self.grid[i_longitude][i_width]["belonging_towers"]:
                    if index == neighboring_tower: continue
                    self.update_graph(neighboring_tower, index)

        row = radius * 2 + 1
        external_row = row + 2
        angles = [0, row + 1, external_row + 2 * row, -1]
        side = self.check_side(index, radius + 1)
        for index_in_list, index_block in enumerate(external_coverage_area):
            if index_in_list in angles: continue
            cords = self.index_in_cords(index_block)
            if side and side != self.check_side(index_block, radius + 1): continue
            if not 0 <= cords["i_width"] < self.city_width \
                    or not 0 <= cords["i_longitude"] < self.city_longitude: continue
            for neighboring_tower in self.grid[cords["i_longitude"]][cords["i_width"]]["belonging_towers"]:
                self.update_graph(neighboring_tower, index)

        if free_square:
            self.free_blocks -= free_square
        return True

    def check_side(self, index, radius):
        side_cords = self.index_in_cords(index)
        if side_cords["i_width"] >= self.city_width - radius:
            return "right"
        elif side_cords["i_width"] <= radius:
            return "left"

    def optimize_towers(self, radius, example=False):
        if not self.free_blocks or len(self.towers_graph.keys()) * self.tower_price + self.tower_price >= self.budget:
            return
        else:
            square = (radius * 2 + 1) ** 2
            best_block = {"index": None, "size_free_square": 0}
            for block in self.free_blocks:
                size_free_square_for_block = 0
                node = block - self.city_width * radius - radius
                side = self.check_side(block, radius)
                free_square = set()
                for _ in range(radius * 2 + 1):
                    row = {node + i for i in range(0, radius * 2 + 1) if
                           not side or side == self.check_side(node + i, radius)}
                    size_free_square_for_block += len(row & self.free_blocks)
                    free_square |= row
                    node += self.city_width
                if size_free_square_for_block == square:
                    self.install_tower(block, radius, free_square)
                    if example: return
                    return self.optimize_towers(radius)
                elif size_free_square_for_block > best_block["size_free_square"]:
                    best_block = {"index": block, "size_free_square": size_free_square_for_block,
                                  "free_square": free_square}
            self.install_tower(best_block["index"], radius, best_block["free_square"])
            if example: return
            return self.optimize_towers(radius)

    def a_star(self, start, target):
        queue = []
        heapq.heappush(queue, (0, start))

        g_scores = {vertex: float('inf') for vertex in self.towers_graph}
        g_scores[start] = 0
        prev_vertices = {}
        while queue:
            current_score, current_vertex = heapq.heappop(queue)
            if current_vertex == target:
                path = []
                while current_vertex in prev_vertices:
                    path.append(current_vertex)
                    current_vertex = prev_vertices[current_vertex]
                path.append(start)
                path.reverse()
                return path

            for neighbor in self.towers_graph[current_vertex]:
                g_score = g_scores[current_vertex] + 1
                h_score = self.manhattan_distance(neighbor, target)
                f_score = g_score + h_score
                if g_score < g_scores[neighbor]:
                    g_scores[neighbor] = g_score
                    prev_vertices[neighbor] = current_vertex
                    heapq.heappush(queue, (f_score, neighbor))
        return []

    def manhattan_distance(self, vertex1, vertex2):
        x1, y1 = divmod(vertex1, 10)
        x2, y2 = divmod(vertex2, 10)
        return abs(x2 - x1) + abs(y2 - y1)


def example_1(n, m, percent_blocked_blocks, budget, tower_price):
    city = CityGrid(n, m, percent_blocked_blocks, budget=budget, tower_price=tower_price)
    city.visual_example(1)
    return city


def example_2(city, radius):
    city.optimize_towers(radius, example=True)
    city.visual_example(2)
    return city


def example_3(city, radius):
    city.optimize_towers(radius)
    city.visual_example(3)
    return city


def example_4(city, first_tower=None, second_tower=None):
    if not first_tower: first_tower = random.choice(list(city.towers_graph.keys()))
    if not second_tower: second_tower = random.choice(list(city.towers_graph.keys()))
    city.visual_example(4, city.a_star(first_tower, second_tower))


city = example_1(n=10, m=10, percent_blocked_blocks=40, budget=340, tower_price=54)
city = example_2(city, radius=1)
city = example_3(city, radius=1)

first_tower, second_tower = None, None
while True:
    example_4(city, first_tower, second_tower)
    first_tower, second_tower = [int(tower_num) for tower_num in re.findall("[0-9]+", input("Введите номера двух "
                                                                                            "башен через пробел "
                                                                                            "\nчтобы построить "
                                                                                            "кратчайший путь между "
                                                                                            "ними\n >>> "))]