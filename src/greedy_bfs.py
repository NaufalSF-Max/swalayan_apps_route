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
        for edge in self.edges:
            u, v, weight = edge
            graph[u].append((v, weight))
            graph[v].append((u, weight))  # Undirected
        return graph

    def heuristic(self, a, b):
        """Heuristic menggunakan jarak Euclidean dari node ke tujuan."""
        x1, y1 = self.nodes[a]
        x2, y2 = self.nodes[b]
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def greedy_bfs(self, start, goal):
        visited = set()
        pq = [(self.heuristic(start, goal), start, [start])]  # (priority, node, path)

        while pq:
            _, current, path = heapq.heappop(pq)
            if current in visited:
                continue
            visited.add(current)

            if current == goal:
                return path

            for neighbor, _ in self.graph.get(current, []):
                if neighbor not in visited:
                    heapq.heappush(pq, (self.heuristic(neighbor, goal), neighbor, path + [neighbor]))
        
        return None  # Jika tidak ditemukan

    def find_nearest_node(self, x, y):
        """Temukan simpul terdekat dari koordinat x, y untuk tujuan produk."""
        nearest = None
        min_dist = float('inf')
        for node, (nx, ny) in self.nodes.items():
            dist = math.sqrt((nx - x)**2 + (ny - y)**2)
            if dist < min_dist:
                nearest = node
                min_dist = dist
        return nearest