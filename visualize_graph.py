import json
import matplotlib.pyplot as plt
import networkx as nx

# Baca dari file JSON
with open("data/toko_graph.json") as f:
    graph_data = json.load(f)

nodes = graph_data['nodes']
edges = graph_data['edges']

# Buat graph
G = nx.Graph()

# Tambahkan node dengan posisi
for node, pos in nodes.items():
    G.add_node(node, pos=tuple(pos))

# Tambahkan edges
G.add_edges_from([tuple(e) for e in edges])

# Ambil posisi
pos = nx.get_node_attributes(G, 'pos')

plt.figure(figsize=(14, 10))

# Gambar lorong (dua garis sejajar)
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]

    dx = x1 - x0
    dy = y1 - y0
    length = (dx**2 + dy**2)**0.5
    offset_x = -dy / length * 0.1
    offset_y = dx / length * 0.1

    # Gambar dua dinding lorong
    plt.plot([x0 + offset_x, x1 + offset_x], [y0 + offset_y, y1 + offset_y], color='black', linewidth=3)
    plt.plot([x0 - offset_x, x1 - offset_x], [y0 - offset_y, y1 - offset_y], color='black', linewidth=3)

    # Placeholder rute (garis tengah)
    plt.plot([x0, x1], [y0, y1], color='lightcoral', linestyle='--', linewidth=1, alpha=0.3)

# Gambar node
nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=900)

# Gambar label
nx.draw_networkx_labels(G, pos, font_size=8)

plt.title("Visualisasi Peta Toko - Lorong Dua Garis", fontsize=14)
plt.axis('off')
plt.tight_layout()
plt.show()