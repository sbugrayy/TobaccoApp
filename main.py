import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QWidget, QScrollArea, QGridLayout, QFrame, QCompleter
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QMouseEvent, QCursor
import json
import os

# Kendi modüllerimizi içe aktarıyoruz
from src.ui_main_window import Ui_MainWindow
from src.database_manager import DatabaseManager
from src.product_manager import ProductManager
from src.kg_calculator import KgCalculator
from styles.main_window_styles import apply_main_window_styles
from styles.card_styles import get_card_stylesheet, get_kg_calculator_stylesheet

# --- Custom Widgets ---
class ProductCard(QFrame):
    def __init__(self, product_data, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self.setFixedSize(220, 250) # Kart boyutu
        self.setObjectName("ProductCard")
        self.setStyleSheet(get_card_stylesheet())

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        self.name_label = QLabel(product_data["name"])
        self.name_label.setObjectName("ProductName")
        self.layout.addWidget(self.name_label)

        self.price_label = QLabel(f"{product_data['price']:.2f} TL")
        self.price_label.setObjectName("ProductPrice")
        self.layout.addWidget(self.price_label)

        if product_data.get("is_kg_sold", False):
            self.kg_label = QLabel("Kiloluk Satış: Evet")
            self.kg_label.setObjectName("ProductKgStatus")
        else:
            self.kg_label = QLabel("Kiloluk Satış: Hayır")
            self.kg_label.setObjectName("ProductKgStatus")
        self.layout.addWidget(self.kg_label)

        self.layout.addStretch() # İçerik dikeyde yukarı hizalanır

        # Animasyon için event filter
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self:
            if event.type() == QMouseEvent.Enter:
                self.setStyleSheet(get_card_stylesheet(hover=True))
                self.setCursor(QCursor(Qt.PointingHandCursor))
            elif event.type() == QMouseEvent.Leave:
                self.setStyleSheet(get_card_stylesheet())
                self.setCursor(QCursor(Qt.ArrowCursor))
        return super().eventFilter(obj, event)

class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yeni Ürün Ekle")
        self.setFixedSize(400, 300)
        self.main_layout = QVBoxLayout(self)

        self.form_layout = QGridLayout()
        self.main_layout.addLayout(self.form_layout)

        self.name_label = QLabel("Ürün Adı:")
        self.name_input = QLineEdit()
        self.form_layout.addWidget(self.name_label, 0, 0)
        self.form_layout.addWidget(self.name_input, 0, 1)

        self.price_label = QLabel("Fiyat (TL):")
        self.price_input = QLineEdit()
        self.price_input.setValidator(QtGui.QDoubleValidator(0.0, 999999.0, 2)) # Sadece ondalıklı sayı girişi
        self.form_layout.addWidget(self.price_label, 1, 0)
        self.form_layout.addWidget(self.price_input, 1, 1)

        self.kg_radio_group = QtWidgets.QButtonGroup(self)
        self.is_kg_sold_label = QLabel("Kiloluk Satılıyor mu?")
        self.yes_radio = QRadioButton("Evet")
        self.no_radio = QRadioButton("Hayır")
        self.no_radio.setChecked(True) # Varsayılan olarak Hayır seçili

        self.kg_radio_group.addButton(self.yes_radio)
        self.kg_radio_group.addButton(self.no_radio)

        self.kg_radio_layout = QHBoxLayout()
        self.kg_radio_layout.addWidget(self.yes_radio)
        self.kg_radio_layout.addWidget(self.no_radio)
        self.form_layout.addWidget(self.is_kg_sold_label, 2, 0)
        self.form_layout.addLayout(self.kg_radio_layout, 2, 1)

        self.main_layout.addStretch()

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.main_layout.addWidget(self.button_box)

    def get_product_data(self):
        name = self.name_input.text().strip()
        price_str = self.price_input.text().strip()
        is_kg_sold = self.yes_radio.isChecked()

        if not name or not price_str:
            return None # Eksik bilgi
        try:
            price = float(price_str)
        except ValueError:
            return None # Geçersiz fiyat

        return {"name": name, "price": price, "is_kg_sold": is_kg_sold}

class KgCalculatorDialog(QDialog):
    def __init__(self, product_name, kg_price, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{product_name} - Kiloluk Hesaplayıcı")
        self.setFixedSize(450, 200)
        self.setStyleSheet(get_kg_calculator_stylesheet())

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        self.kg_price = kg_price

        self.price_info_label = QLabel(f"<b>1 KG Fiyatı:</b> {kg_price:.2f} TL")
        self.price_info_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.price_info_label)

        self.input_layout = QHBoxLayout()
        self.main_layout.addLayout(self.input_layout)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Değer Girin...")
        self.input_field.setValidator(QtGui.QDoubleValidator(0.0, 999999.0, 2))
        self.input_field.textChanged.connect(self.calculate_result)
        self.input_field.setObjectName("KgCalculatorInput")
        self.input_layout.addWidget(self.input_field)

        self.toggle_button = QPushButton("Gram/Para")
        self.toggle_button.setObjectName("ToggleButton")
        self.toggle_button.setCheckable(True) # Toggle özelliği eklendi
        self.toggle_button.setChecked(True) # Başlangıçta Gram olarak ayarlı
        self.toggle_button.clicked.connect(self.update_placeholder)
        self.input_layout.addWidget(self.toggle_button)

        self.result_label = QLabel("Sonuç: ")
        self.result_label.setObjectName("KgCalculatorResult")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.result_label)

        self.update_placeholder() # Başlangıç placeholder'ını ayarla

    def update_placeholder(self):
        if self.toggle_button.isChecked():
            self.input_field.setPlaceholderText("Miktar (gr)")
        else:
            self.input_field.setPlaceholderText("Tutar (TL)")
        self.calculate_result() # Placeholder değişince yeniden hesapla

    def calculate_result(self):
        try:
            value = float(self.input_field.text())
            if self.toggle_button.isChecked(): # Gram hesaplama
                result_price = KgCalculator.calculate_price_from_grams(self.kg_price, value)
                self.result_label.setText(f"Sonuç: {value:.2f} gr = {result_price:.2f} TL")
            else: # Para hesaplama
                result_grams = KgCalculator.calculate_grams_from_price(self.kg_price, value)
                self.result_label.setText(f"Sonuç: {value:.2f} TL = {result_grams:.2f} gr")
        except ValueError:
            self.result_label.setText("Sonuç: Geçersiz giriş")
        except ZeroDivisionError:
            self.result_label.setText("Sonuç: Kilogram fiyatı sıfır olamaz!")

class TobaccoApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        apply_main_window_styles(self) # Ana pencere stilini uygula

        self.db_manager = DatabaseManager(os.path.join("data", "products.json"))
        self.product_manager = ProductManager(self.db_manager)

        self.load_products()
        self.setup_connections()
        self.setup_autocomplete()

    def setup_connections(self):
        self.add_product_button.clicked.connect(self.open_add_product_dialog)
        self.search_input.textChanged.connect(self.filter_products)

    def setup_autocomplete(self):
        product_names = [p["name"] for p in self.product_manager.get_all_products()]
        self.completer_model = QStringListModel()
        self.completer_model.setStringList(product_names)
        self.completer = QCompleter(self.completer_model, self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.search_input.setCompleter(self.completer)

    def load_products(self):
        # Mevcut kartları temizle
        while self.product_grid_layout.count():
            item = self.product_grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        products = self.product_manager.get_all_products()
        row = 0
        col = 0
        for product in products:
            card = ProductCard(product)
            self.product_grid_layout.addWidget(card, row, col)
            if product.get("is_kg_sold", False):
                card.mousePressEvent = lambda event, p=product: self.open_kg_calculator(event, p) # Mouse click event ekle
            col += 1
            if col >= 4: # Her satırda 4 kart
                col = 0
                row += 1

    def open_add_product_dialog(self):
        dialog = AddProductDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            product_data = dialog.get_product_data()
            if product_data:
                self.product_manager.add_product(product_data)
                self.load_products() # Ürünleri yeniden yükle
                self.setup_autocomplete() # Arama çubuğunu güncelle
            else:
                QtWidgets.QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun ve geçerli bir fiyat girin.")

    def open_kg_calculator(self, event, product_data):
        if event.button() == Qt.LeftButton: # Sadece sol tıklamada aç
            dialog = KgCalculatorDialog(product_data["name"], product_data["price"], self)
            dialog.exec_()

    def filter_products(self):
        search_text = self.search_input.text().lower()
        products = self.product_manager.get_all_products()

        # Mevcut kartları temizle
        while self.product_grid_layout.count():
            item = self.product_grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        row = 0
        col = 0
        for product in products:
            if search_text in product["name"].lower():
                card = ProductCard(product)
                self.product_grid_layout.addWidget(card, row, col)
                if product.get("is_kg_sold", False):
                    card.mousePressEvent = lambda event, p=product: self.open_kg_calculator(event, p)
                col += 1
                if col >= 4:
                    col = 0
                    row += 1
        # Layout'u güncelle
        self.product_grid_layout.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TobaccoApp()
    window.show()
    sys.exit(app.exec_())