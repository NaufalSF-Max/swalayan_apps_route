import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import networkx as nx
from math import sqrt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Data Map & Barang ---
nodes = {
    'A': (0, 0),
    'B': (2, 0),
    'C': (4, 0),
    'D': (0, 2),
    'E': (2, 2),
    'F': (4, 2),
    'G': (0, 4),
    'H': (2, 4),
    'I': (4, 4),
}

edges = [
    ('A', 'B'), ('B', 'C'),
    ('A', 'D'), ('B', 'E'), ('C', 'F'),
    ('D', 'E'), ('E', 'F'),
    ('D', 'G'), ('E', 'H'), ('F', 'I'),
    ('G', 'H'), ('H', 'I')
]

barang_lokasi = {
    'Susu': 'F',
    'Roti': 'H',
    'Telur': 'G',
    'Sabun': 'C'
}

# --- Heuristik (Jarak Euclidean) ---
def heuristik(a, b):
    (x1, y1) = nodes[a]
    (x2, y2) = nodes[b]
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

# --- Greedy Best First Search ---
def greedy_best_first_search(start, goal):
    from queue import PriorityQueue
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {}
    came_from[start] = None

    while not frontier.empty():
        _, current = frontier.get()
        if current == goal:
            break
        for neighbor in graph.neighbors(current):
            if neighbor not in came_from:
                priority = heuristik(goal, neighbor)
                frontier.put((priority, neighbor))
                came_from[neighbor] = current

    # rekonstruksi jalur
    path = []
    node = goal
    while node != start:
        path.append(node)
        node = came_from.get(node)
        if node is None:
            return []
    path.append(start)
    path.reverse()
    return path

# --- UI Functions ---
def cari_barang():
    barang = barang_cb.get()
    tujuan = barang_lokasi.get(barang)
    start = 'A'  # Titik awal pembeli
    path = greedy_best_first_search(start, tujuan)
    tampilkan_rute(path)

def tampilkan_rute(path):
    ax.clear()
    pos = nodes

    nx.draw(graph, pos, ax=ax, with_labels=True, node_color='lightblue', node_size=800)
    if path:
        edge_list = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(graph, pos, edgelist=edge_list, edge_color='r', width=3, ax=ax)
    canvas.draw()

# --- UI Utama ---
root = tk.Tk()
root.title("Pencarian Barang di Swalayan")

frame = ttk.Frame(root, padding=10)
frame.pack()

ttk.Label(frame, text="Pilih Barang:").grid(row=0, column=0)
barang_cb = ttk.Combobox(frame, values=list(barang_lokasi.keys()))
barang_cb.grid(row=0, column=1)
barang_cb.current(0)

ttk.Button(frame, text="Cari Lokasi", command=cari_barang).grid(row=0, column=2)

# --- Grafik Peta Toko ---
fig, ax = plt.subplots(figsize=(5, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# --- Graph Preparation ---
graph = nx.Graph()
graph.add_nodes_from(nodes)
graph.add_edges_from(edges)

tampilkan_rute([])

root.mainloop()