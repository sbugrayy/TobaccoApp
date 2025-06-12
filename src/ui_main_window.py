from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700) # Pencere boyutu
        MainWindow.setStyleSheet("background-color: #f0f0f0;") # Genel arka plan rengi

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)
        self.main_layout.setObjectName("main_layout")

        # Üst Kısım: Arama Çubuğu ve Yeni Ürün Ekleme
        self.header_frame = QtWidgets.QFrame(self.centralwidget)
        self.header_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.header_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.header_frame.setObjectName("header_frame")
        self.header_layout = QtWidgets.QHBoxLayout(self.header_frame)
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setObjectName("header_layout")

        self.search_input = QtWidgets.QLineEdit(self.header_frame)
        self.search_input.setPlaceholderText("Ürün Ara...")
        self.search_input.setObjectName("search_input")
        self.header_layout.addWidget(self.search_input)

        self.add_product_button = QtWidgets.QPushButton(self.header_frame)
        self.add_product_button.setText("Yeni Ürün Ekle")
        self.add_product_button.setObjectName("add_product_button")
        self.header_layout.addWidget(self.add_product_button)
        self.main_layout.addWidget(self.header_frame)

        # Ürün Görüntüleme Alanı
        self.scroll_area = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area_widget_contents = QtWidgets.QWidget()
        self.scroll_area_widget_contents.setObjectName("scroll_area_widget_contents")
        self.product_grid_layout = QtWidgets.QGridLayout(self.scroll_area_widget_contents)
        self.product_grid_layout.setContentsMargins(5, 5, 5, 5)
        self.product_grid_layout.setSpacing(10)
        self.product_grid_layout.setObjectName("product_grid_layout")
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.main_layout.addWidget(self.scroll_area)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tütün Fiyat Uygulaması"))