import json
import heapq
import math

class GreedyBFS:
    def __init__(self, graph_file):
        with open(graph_file, 'r') as f:
            data = json.load(f)

        self.nodes = data['nodes']
        self.edges = data['edges']
        self.graph = self.build_graph()

    def build_graph(self):
        graph = {node: [] for node in self.nodes}
        for u, v, w in self.edges:
            graph[u].append((v, w))
            graph[v].append((u, w))
        return graph

    def heuristic(self, a, b):
        x1, y1 = self.nodes[a]
        x2, y2 = self.nodes[b]
        return math.hypot(x1 - x2, y1 - y2)

    def greedy_bfs(self, start, goal):
        visited = set()
        heap = [(self.heuristic(start, goal), start, [start])]
        while heap:
            _, current, path = heapq.heappop(heap)
            if current == goal:
                return path
            if current in visited:
                continue
            visited.add(current)
            for neighbor, _ in self.graph.get(current, []):
                if neighbor not in visited:
                    heapq.heappush(heap, (self.heuristic(neighbor, goal), neighbor, path + [neighbor]))
        return None

    def a_star(self, start, goal):
        open_set = [(0 + self.heuristic(start, goal), 0, start, [start])]  # (f, g, current, path)
        visited = set()

        while open_set:
            f, g, current, path = heapq.heappop(open_set)

            if current == goal:
                return path

            if current in visited:
                continue
            visited.add(current)

            for neighbor, cost in self.graph.get(current, []):
                if neighbor not in visited:
                    new_g = g + cost
                    new_f = new_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (new_f, new_g, neighbor, path + [neighbor]))

        return None

    def find_nearest_node(self, x, y):
        nearest = None
        min_dist = float('inf')
        for node, (nx, ny) in self.nodes.items():
            dist = math.hypot(x - nx, y - ny)
            if dist < min_dist:
                nearest = node
                min_dist = dist
        return nearest