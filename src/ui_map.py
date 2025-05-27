# src/ui_map.py
import json
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from src.greedy_bfs import GreedyBFS

class MapWindow(QWidget):
    def __init__(self, product_name, back_callback=None):
        super().__init__()
        self.setWindowTitle("Peta Lokasi Produk")
        self.setMinimumSize(800, 600)
        self.product_name = product_name
        self.back_callback = back_callback

        # Tambahkan pemanggilan style
        with open("resources/style.css") as f:
            self.setStyleSheet(f.read())

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.canvas = FigureCanvas(plt.Figure(figsize=(8, 6)))
        layout.addWidget(self.canvas)

        # Tombol kembali di kanan bawah
        button_layout = QHBoxLayout()
        self.back_button = QPushButton("Kembali")
        self.back_button.setObjectName("backButton")
        self.back_button.clicked.connect(self.kembali)
        button_layout.addStretch()
        button_layout.addWidget(self.back_button)
        layout.addLayout(button_layout)

        self.gbfs = GreedyBFS("data/toko_graph.json")
        self.plot_map()

    def kembali(self):
        self.close()
        if self.back_callback:
            self.back_callback()

    def plot_map(self):
        ax = self.canvas.figure.add_subplot(111)
        ax.clear()

        with open("data/toko_graph.json") as f:
            graph_data = json.load(f)

        pos = {k: tuple(v) for k, v in graph_data["nodes"].items()}
        edges = [tuple(e[:2]) for e in graph_data["edges"]]

        G = nx.Graph()
        G.add_nodes_from(pos.keys())
        for e in graph_data["edges"]:
            G.add_edge(e[0], e[1], weight=e[2])

        # Lorong hitam (dinding)
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            dx, dy = x1 - x0, y1 - y0
            length = (dx ** 2 + dy ** 2) ** 0.5
            offset_x = -dy / length * 0.1
            offset_y = dx / length * 0.1

            ax.plot([x0 + offset_x, x1 + offset_x], [y0 + offset_y, y1 + offset_y], color='black', linewidth=3)
            ax.plot([x0 - offset_x, x1 - offset_x], [y0 - offset_y, y1 - offset_y], color='black', linewidth=3)
            ax.plot([x0, x1], [y0, y1], color='lightcoral', linestyle='--', linewidth=1, alpha=0.3)

        # Ukuran node kecil untuk T1-T28
        sizes = [0 if node.startswith("T") else 700 for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=sizes, ax=ax)

        # Label hanya untuk lokasi (bukan T1–T28 atau Start)
        labels = {node: node for node in G.nodes() if not node.startswith("T") and node != "Start"}
        nx.draw_networkx_labels(G, pos, labels, font_size=8, ax=ax)

        cost_text = ""

        # Tandai lokasi produk dan jalur
        if self.product_name in pos:
            x, y = pos[self.product_name]
            ax.scatter(x, y, color='red', s=250, label='Lokasi Produk', zorder=5)
            ax.annotate(self.product_name, (x, y + 0.3), fontsize=10, color='red', ha='center')

            nearest_node = self.gbfs.find_nearest_node(x, y)
            gbfs_path = self.gbfs.greedy_bfs("Start", nearest_node)
            a_star_path = self.gbfs.a_star("Start", nearest_node)

            def calculate_path_cost(path):
                total = 0
                for i in range(len(path) - 1):
                    for u, v, w in graph_data["edges"]:
                        if (u == path[i] and v == path[i+1]) or (v == path[i] and u == path[i+1]):
                            total += w
                            break
                return total

            # Gambar jalur GBFS
            if gbfs_path:
                for i in range(len(gbfs_path) - 1):
                    n1, n2 = gbfs_path[i], gbfs_path[i + 1]
                    x1, y1 = pos[n1]
                    x2, y2 = pos[n2]
                    ax.plot([x1, x2], [y1, y2], color='red', linewidth=3, zorder=4)

                gbfs_cost = calculate_path_cost(gbfs_path)
                cost_text += f"Greedy BFS Cost: {gbfs_cost:.2f}"

            if a_star_path:
                a_star_cost = calculate_path_cost(a_star_path)
                cost_text += f"\nA* Search Cost: {a_star_cost:.2f}"

            # Tampilkan di UI
            if cost_text:
                ax.text(0.95, 0.05, cost_text,
                        transform=ax.transAxes,
                        fontsize=9,
                        verticalalignment='bottom',
                        horizontalalignment='right',
                        bbox=dict(facecolor='white', edgecolor='gray', alpha=0.8))

        # Ganti ikon start
        if "Start" in pos:
            x, y = pos["Start"]
            try:
                start_icon_path = "assets/icons/start_icon.jpg"
                icon_size = 0.11
                icon_img = plt.imread(start_icon_path)
                icon = OffsetImage(icon_img, zoom=icon_size)
                ab = AnnotationBbox(icon, (x, y), frameon=False, zorder=6)
                ax.add_artist(ab)
            except FileNotFoundError:
                ax.annotate("Start", (x, y), fontsize=10, color='blue', ha='center')

        ax.set_title("Peta Toko", fontsize=14)
        ax.axis('off')
        ax.legend()
        self.canvas.draw()