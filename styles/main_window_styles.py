def apply_main_window_styles(window):
    window.setStyleSheet("""
        QMainWindow {
            background-color: #f0f2f5; /* Açık gri arka plan */
            font-family: 'Segoe UI', sans-serif;
            color: #333;
        }

        /* Başlık Çubuğu ve Yeni Ürün Ekle Butonu */
        QFrame#header_frame {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        QLineEdit#search_input {
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            background-color: #f8f8f8;
            color: #555;
        }

        QLineEdit#search_input:focus {
            border: 1px solid #007bff;
            background-color: #ffffff;
        }

        QPushButton#add_product_button {
            background-color: #28a745; /* Yeşil buton */
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            transition: background-color 0.3s ease; /* Hover efekti için geçiş */
        }

        QPushButton#add_product_button:hover {
            background-color: #218838; /* Koyu yeşil hover */
        }

        /* Scroll Alanı */
        QScrollArea {
            border: none;
        }

        QScrollArea > QWidget > QWidget { /* scroll_area_widget_contents */
            background-color: #f0f2f5;
        }

        QScrollBar:vertical {
            border: none;
            background: #e0e0e0;
            width: 8px;
            margin: 0px 0px 0px 0px;
        }

        QScrollBar::handle:vertical {
            background: #c0c0c0;
            min-height: 20px;
            border-radius: 4px;
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
        }
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }

        /* Ürün Ekleme Diyaloğu */
        QDialog {
            background-color: #ffffff;
            border-radius: 10px;
        }
        QDialog QLabel {
            font-size: 15px;
            font-weight: 500;
            color: #444;
        }
        QDialog QLineEdit {
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 14px;
        }
        QDialog QLineEdit:focus {
            border: 1px solid #007bff;
        }
        QDialog QRadioButton {
            font-size: 14px;
            color: #555;
            padding: 5px 0;
        }
        QDialog QPushButton {
            background-color: #007bff;
            color: white;
            padding: 8px 15px;
            border: none;
            border-radius: 5px;
            font-size: 14px;
        }
        QDialog QPushButton:hover {
            background-color: #0056b3;
        }
    """)