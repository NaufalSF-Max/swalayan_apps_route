# src/ui_main.py

import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Peta Toko Swalayan")
        self.resize(1000, 600)
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout(self)

        # Sidebar kategori
        self.sidebar = QVBoxLayout()
        self.sidebar.setSpacing(10)
        self.sidebar.setAlignment(Qt.AlignTop)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setLayout(self.sidebar)
        scroll_area.setWidget(scroll_content)

        # Grid produk
        self.product_area = QVBoxLayout()
        self.product_area.setAlignment(Qt.AlignTop)

        product_scroll = QScrollArea()
        product_scroll.setWidgetResizable(True)
        self.product_widget = QWidget()
        self.product_widget.setLayout(self.product_area)
        product_scroll.setWidget(self.product_widget)

        main_layout.addWidget(scroll_area, 2)
        main_layout.addWidget(product_scroll, 5)

        self.load_categories()

    def load_categories(self):
        try:
            with open("data/produk.json", "r", encoding="utf-8") as f:
                self.produk_data = json.load(f)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "File produk.json tidak ditemukan!")
            return

        self.sidebar_buttons = []
        for kategori in self.produk_data:
            btn = QPushButton(kategori)
            btn.clicked.connect(lambda checked, k=kategori: self.show_products(k))
            self.sidebar.addWidget(btn)
            self.sidebar_buttons.append(btn)

    def show_products(self, kategori):
        for i in reversed(range(self.product_area.count())):
            widget = self.product_area.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        produk_list = self.produk_data.get(kategori, [])
        for produk in produk_list:
            frame = QFrame()
            frame.setFrameShape(QFrame.Box)
            layout = QVBoxLayout()
            layout.setAlignment(Qt.AlignCenter)

            # Nama Produk
            nama = QLabel(produk["nama"])
            nama.setAlignment(Qt.AlignCenter)
            layout.addWidget(nama)

            # Gambar Produk
            gambar_path = produk.get("gambar", "assets/placeholder.png")
            if os.path.exists(gambar_path):
                pixmap = QPixmap(gambar_path).scaled(150, 150, Qt.KeepAspectRatio)
            else:
                pixmap = QPixmap("assets/placeholder.png").scaled(150, 150, Qt.KeepAspectRatio)

            gambar = QLabel()
            gambar.setPixmap(pixmap)
            gambar.setAlignment(Qt.AlignCenter)
            layout.addWidget(gambar)

            # Tombol Lihat Lokasi
            btn_lokasi = QPushButton("Lihat Lokasi")
            btn_lokasi.clicked.connect(lambda checked, lokasi=produk["lokasi"]: self.tunjukkan_lokasi(lokasi))
            layout.addWidget(btn_lokasi)

            frame.setLayout(layout)
            self.product_area.addWidget(frame)

    def tunjukkan_lokasi(self, lokasi):
        QMessageBox.information(self, "Lokasi Produk", f"Produk ini berada di blok: {lokasi}")