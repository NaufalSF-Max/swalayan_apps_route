import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

# Data dummy awal
produk_data = [
    {"nama": "Sampo", "kategori": "Peralatan Mandi", "lokasi": "Peralatan Mandi"},
    {"nama": "Mangga", "kategori": "Buah", "lokasi": "Buah"},
    {"nama": "Daging Sapi", "kategori": "Daging", "lokasi": "Daging"},
    {"nama": "Wortel", "kategori": "Sayuran", "lokasi": "Sayuran"},
    {"nama": "Susu UHT", "kategori": "Produk Susu", "lokasi": "Produk Susu"},
    # Tambahkan lebih banyak sesuai data
]

kategori_data = sorted(list(set(p['kategori'] for p in produk_data)))

def show_location(lokasi):
    print(f"Navigasi ke lokasi: {lokasi}")
    # nanti dihubungkan ke halaman peta swalayan

root = tk.Tk()
root.title("Pencarian Barang Swalayan")
root.geometry("1024x600")

# ========================= Frame Utama =========================
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Scrollbar vertikal halaman utama
canvas = tk.Canvas(main_frame)
scroll_y = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)

canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_y.pack(side=tk.LEFT, fill=tk.Y)

# ========================= Search Bar =========================
search_frame = tk.Frame(scrollable_frame, pady=10)
search_frame.pack(fill=tk.X, padx=10)

search_entry = tk.Entry(search_frame, font=("Arial", 14), width=40)
search_entry.pack(side=tk.LEFT, padx=(0, 10))

search_icon = tk.Button(search_frame, text="🔍", font=("Arial", 14))
search_icon.pack(side=tk.LEFT)

# ========================= Konten Grid =========================
content_frame = tk.Frame(scrollable_frame)
content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

def tampilkan_produk():
    for widget in content_frame.winfo_children():
        widget.destroy()

    kolom = 3
    for i, item in enumerate(produk_data):
        frame = tk.Frame(content_frame, relief=tk.RAISED, bd=2, padx=10, pady=10)
        frame.grid(row=i//kolom, column=i%kolom, padx=5, pady=5)

        tk.Label(frame, text=item['nama'], font=("Arial", 12, "bold")).pack()
        img = ImageTk.PhotoImage(Image.new("RGB", (100, 70), color='gray'))  # placeholder
        tk.Label(frame, image=img).pack()
        frame.image = img  # simpan referensi

        tk.Button(frame, text="Lihat Lokasi", command=lambda l=item['lokasi']: show_location(l)).pack(pady=5)

tampilkan_produk()

# ========================= Sidebar Kategori =========================
sidebar_frame = tk.Frame(scrollable_frame, width=200)
sidebar_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 10))

sidebar_label = tk.Label(sidebar_frame, text="Kategori", font=("Arial", 14, "bold"))
sidebar_label.pack(pady=5)

kategori_canvas = tk.Canvas(sidebar_frame, width=180, height=400)
kategori_scrollbar = tk.Scrollbar(sidebar_frame, orient="vertical", command=kategori_canvas.yview)
kategori_container = tk.Frame(kategori_canvas)

kategori_container.bind(
    "<Configure>",
    lambda e: kategori_canvas.configure(
        scrollregion=kategori_canvas.bbox("all")
    )
)

kategori_canvas.create_window((0, 0), window=kategori_container, anchor="nw")
kategori_canvas.configure(yscrollcommand=kategori_scrollbar.set)

kategori_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
kategori_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def filter_by_kategori(kat):
    global produk_data
    produk_data_filtered = [p for p in produk_data if p['kategori'] == kat]
    tampilkan_produk_dari_data(produk_data_filtered)

def tampilkan_produk_dari_data(data):
    for widget in content_frame.winfo_children():
        widget.destroy()

    kolom = 3
    for i, item in enumerate(data):
        frame = tk.Frame(content_frame, relief=tk.RAISED, bd=2, padx=10, pady=10)
        frame.grid(row=i//kolom, column=i%kolom, padx=5, pady=5)

        tk.Label(frame, text=item['nama'], font=("Arial", 12, "bold")).pack()
        img = ImageTk.PhotoImage(Image.new("RGB", (100, 70), color='gray'))  # placeholder
        tk.Label(frame, image=img).pack()
        frame.image = img

        tk.Button(frame, text="Lihat Lokasi", command=lambda l=item['lokasi']: show_location(l)).pack(pady=5)

for kat in kategori_data:
    btn = tk.Button(kategori_container, text=kat, width=20, command=lambda k=kat: filter_by_kategori(k))
    btn.pack(pady=2)

root.mainloop()
