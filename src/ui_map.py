# src/ui_map.py
import json
import networkx as nx
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from greedy_bfs import GreedyBFS  # Tambahkan ini

class MapWindow(QWidget):
    def __init__(self, product_name, back_callback=None):
        super().__init__()
        self.setWindowTitle("Peta Lokasi Produk")
        self.setMinimumSize(800, 600)
        self.product_name = product_name
        self.back_callback = back_callback

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.canvas = FigureCanvas(plt.Figure(figsize=(8, 6)))
        layout.addWidget(self.canvas)

        self.gbfs = GreedyBFS("data/toko_graph.json")  # Inisialisasi algoritma

        self.plot_map()

    def plot_map(self):
        ax = self.canvas.figure.add_subplot(111)
        ax.clear()

        # Load graph
        with open("data/toko_graph.json") as f:
            graph_data = json.load(f)

        pos = {k: tuple(v) for k, v in graph_data["nodes"].items()}
        edges = [tuple(e[:2]) for e in graph_data["edges"]]  # Abaikan bobot jika ada

        G = nx.Graph()
        G.add_nodes_from(pos.keys())
        G.add_edges_from(edges)

        # Gambar lorong sebagai dua garis sejajar
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            dx, dy = x1 - x0, y1 - y0
            length = (dx**2 + dy**2)**0.5
            offset_x = -dy / length * 0.1
            offset_y = dx / length * 0.1

            ax.plot([x0 + offset_x, x1 + offset_x], [y0 + offset_y, y1 + offset_y], color='black', linewidth=3)
            ax.plot([x0 - offset_x, x1 - offset_x], [y0 - offset_y, y1 - offset_y], color='black', linewidth=3)
            ax.plot([x0, x1], [y0, y1], color='lightcoral', linestyle='--', linewidth=1, alpha=0.3)

        # Gambar node
        nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)

        # Tandai lokasi produk
        if self.product_name in pos:
            x, y = pos[self.product_name]
            ax.scatter(x, y, color='red', s=250, label='Lokasi Produk', zorder=5)
            ax.annotate(self.product_name, (x, y + 0.3), fontsize=10, color='red', ha='center')

            # Cari node terdekat dan gambar jalur dengan Greedy BFS
            nearest_node = self.gbfs.find_nearest_node(x, y)
            path = self.gbfs.greedy_bfs("Start", nearest_node)

            if path:
                for i in range(len(path) - 1):
                    n1, n2 = path[i], path[i + 1]
                    x1, y1 = pos[n1]
                    x2, y2 = pos[n2]
                    ax.plot([x1, x2], [y1, y2], color='red', linewidth=3, zorder=4)

        ax.set_title("Peta Toko", fontsize=14)
        ax.axis('off')
        ax.legend()
        self.canvas.draw()