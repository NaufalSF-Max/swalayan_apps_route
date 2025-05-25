import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QLineEdit, QListWidget, QListWidgetItem, QSizePolicy,
    QGridLayout, QListView
)
from PyQt5.QtGui import QPixmap, QColor, QPalette
from PyQt5.QtCore import Qt, QSize, QTimer

from ui_map import MapWindow  # Import jendela peta

class ProductItem(QWidget):
    def __init__(self, product_data, parent_window=None):
        super().__init__()
        self.product_data = product_data
        self.parent_window = parent_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(8)

        name_label = QLabel(self.product_data['nama'])
        name_label.setAlignment(Qt.AlignCenter)

        image_label = QLabel()
        pixmap = QPixmap(self.product_data['gambar'])
        image_label.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)

        button = QPushButton("Lihat Lokasi")
        button.setObjectName("lokasiButton")
        button.clicked.connect(self.lihat_lokasi)

        layout.addWidget(name_label)
        layout.addWidget(image_label)
        layout.addWidget(button)
        self.setLayout(layout)
        self.setFixedSize(200, 250)
        self.setObjectName("productItem")

    def lihat_lokasi(self):
        lokasi = self.product_data.get('lokasi')
        if lokasi:
            self.map_window = MapWindow(product_name=lokasi)
            self.map_window.show()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Swalayan")
        self.resize(1000, 600)
        self.all_products = self.load_products()
        self.filtered_products = self.all_products.copy()
        self.selected_category = None
        self.init_ui()

    def load_products(self):
        with open("data/produk.json", "r") as f:
            data = json.load(f)
            products = []
            for kategori, daftar_produk in data.items():
                for produk in daftar_produk:
                    produk['kategori'] = kategori
                    products.append(produk)
            return products

    def init_ui(self):
        self.setObjectName("mainWindow")
        self.setStyleSheet(open("resources/style.css").read())

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#f2f6f9"))
        self.setPalette(palette)

        main_layout = QHBoxLayout(self)

        # Sidebar
        self.sidebar = QWidget()
        self.sidebar.setMinimumWidth(255)
        self.sidebar.setMaximumWidth(300)
        self.sidebar.setStyleSheet("background-color: #f7fbfd;")
        sidebar_layout = QVBoxLayout(self.sidebar)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari produk...")
        self.search_input.textChanged.connect(self.search_products)
        sidebar_layout.addWidget(self.search_input)

        self.kategori_list = QListWidget()
        self.kategori_list.setViewMode(QListView.IconMode)
        self.kategori_list.setSpacing(6)
        self.kategori_list.setObjectName("kategoriList")
        self.kategori_list.itemClicked.connect(self.filter_by_kategori)
        sidebar_layout.addWidget(self.kategori_list)

        self.load_kategori()

        # Area Produk
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setContentsMargins(20, 20, 20, 20)
        self.grid_layout.setSpacing(16)
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.scroll_area.setWidget(self.grid_widget)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.scroll_area)

        self.populate_products()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.populate_products()

    def load_kategori(self):
        kategori_set = set()
        for p in self.all_products:
            if isinstance(p, dict) and 'kategori' in p:
                kategori_set.add(p['kategori'])

        for kategori in sorted(kategori_set):
            item = QListWidgetItem(kategori)
            self.kategori_list.addItem(item)

    def filter_by_kategori(self, item):
        kategori = item.text()
        if self.selected_category == kategori:
            self.selected_category = None
            self.filtered_products = self.all_products.copy()
            self.kategori_list.clearSelection()
        else:
            self.selected_category = kategori
            self.filtered_products = [p for p in self.all_products if p.get('kategori') == kategori]
        self.search_input.clear()
        self.populate_products()

    def search_products(self):
        keyword = self.search_input.text().lower()
        if keyword:
            self.filtered_products = [p for p in self.all_products if keyword in p.get('nama', '').lower()]
            self.kategori_list.clearSelection()
            self.selected_category = None
        else:
            self.filtered_products = self.all_products.copy()
        self.populate_products()

    def populate_products(self):
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        width = self.scroll_area.viewport().width()
        columns = 4 if width > 900 else 3 if width > 600 else 1

        row = col = 0
        for product in self.filtered_products:
            item = ProductItem(product, parent_window=self)
            self.grid_layout.addWidget(item, row, col)
            col += 1
            if col >= columns:
                col = 0
                row += 1

        QTimer.singleShot(0, lambda: self.scroll_area.verticalScrollBar().setValue(0))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())