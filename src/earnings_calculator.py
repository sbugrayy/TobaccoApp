from PyQt5 import QtWidgets
from datetime import datetime
import json
from styles.earnings_styles import EARNINGS_FRAME_STYLE

class EarningsCalculator:
    def __init__(self, parent=None):
        self.parent = parent
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        # Ana frame
        self.earnings_frame = QtWidgets.QFrame(self.parent)
        self.earnings_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.earnings_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.earnings_frame.setObjectName("earnings_frame")
        self.earnings_frame.setStyleSheet(EARNINGS_FRAME_STYLE)
        
        # Layout
        self.earnings_layout = QtWidgets.QHBoxLayout(self.earnings_frame)
        self.earnings_layout.setContentsMargins(15, 15, 15, 15)
        self.earnings_layout.setSpacing(15)
        
        # Kazanç Girişi
        self.earnings_input = QtWidgets.QLineEdit(self.earnings_frame)
        self.earnings_input.setPlaceholderText("Kazanç Miktarı (TL)")
        self.earnings_input.setObjectName("earnings_input")
        self.earnings_layout.addWidget(self.earnings_input)
        
        # Kazanç Ekleme Butonu
        self.add_earnings_button = QtWidgets.QPushButton(self.earnings_frame)
        self.add_earnings_button.setText("Kazanç Ekle")
        self.add_earnings_button.setObjectName("add_earnings_button")
        self.earnings_layout.addWidget(self.add_earnings_button)
        
        # Günlük Toplam Butonu
        self.show_daily_total_button = QtWidgets.QPushButton(self.earnings_frame)
        self.show_daily_total_button.setText("Günlük Toplamı Göster")
        self.show_daily_total_button.setObjectName("show_daily_total_button")
        self.earnings_layout.addWidget(self.show_daily_total_button)

        # Aylık Toplam Butonu
        self.show_monthly_total_button = QtWidgets.QPushButton(self.earnings_frame)
        self.show_monthly_total_button.setText("Aylık Toplamı Göster")
        self.show_monthly_total_button.setObjectName("show_daily_total_button")
        self.earnings_layout.addWidget(self.show_monthly_total_button)
        
        # Verileri Sıfırlama Butonu
        self.reset_earnings_button = QtWidgets.QPushButton(self.earnings_frame)
        self.reset_earnings_button.setText("Verileri Sıfırla")
        self.reset_earnings_button.setObjectName("reset_earnings_button")
        self.reset_earnings_button.setStyleSheet("""
            QPushButton#reset_earnings_button {
                background-color: #dc3545;
            }
            QPushButton#reset_earnings_button:hover {
                background-color: #c82333;
            }
        """)
        self.earnings_layout.addWidget(self.reset_earnings_button)
        
        # Günlük Toplam Label
        self.daily_total_label = QtWidgets.QLabel(self.earnings_frame)
        self.daily_total_label.setText("Günlük Toplam: --.-- TL")
        self.daily_total_label.setObjectName("daily_total_label")
        self.earnings_layout.addWidget(self.daily_total_label)

        # Aylık Toplam Label
        self.monthly_total_label = QtWidgets.QLabel(self.earnings_frame)
        self.monthly_total_label.setText("Aylık Toplam: --.-- TL")
        self.monthly_total_label.setObjectName("daily_total_label")
        self.earnings_layout.addWidget(self.monthly_total_label)

    def connect_signals(self):
        self.add_earnings_button.clicked.connect(self.add_earnings)
        self.show_daily_total_button.clicked.connect(self.show_daily_total)
        self.show_monthly_total_button.clicked.connect(self.show_monthly_total)
        self.reset_earnings_button.clicked.connect(self.reset_earnings)

    def add_earnings(self):
        try:
            amount = float(self.earnings_input.text())
            if amount <= 0:
                QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen geçerli bir miktar girin!")
                return
                
            # JSON dosyasına kazancı ekle
            with open("data/daily_earnings.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            data["earnings"].append({
                "amount": amount,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            with open("data/daily_earnings.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            self.earnings_input.clear()
            self.daily_total_label.setText("Günlük Toplam: --.-- TL")  # Toplamı sıfırla
            
        except ValueError:
            QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen geçerli bir sayı girin!")

    def show_daily_total(self):
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            total = 0.0
            
            with open("data/daily_earnings.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for earning in data["earnings"]:
                if earning["date"].startswith(today):
                    total += earning["amount"]
            
            self.daily_total_label.setText(f"Günlük Toplam: {total:.2f} TL")
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Hata", f"Toplam hesaplanırken bir hata oluştu: {str(e)}")

    def show_monthly_total(self):
        try:
            month = datetime.now().strftime("%Y-%m")
            total = 0.0

            with open("data/daily_earnings.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            for earning in data["earnings"]:
                if earning["date"].startswith(month):
                    total += earning["amount"]

            self.monthly_total_label.setText(f"Aylık Toplam: {total:.2f} TL")

        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Hata", f"Toplam hesaplanırken bir hata oluştu: {str(e)}")

    def reset_earnings(self):
        reply = QtWidgets.QMessageBox.question(
            None, 
            'Onay', 
            'Tüm kazanç verilerini sıfırlamak istediğinizden emin misiniz?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                # JSON dosyasını sıfırla
                with open("data/daily_earnings.json", "w", encoding="utf-8") as f:
                    json.dump({"earnings": []}, f, indent=4, ensure_ascii=False)
                
                # Arayüzü güncelle
                self.daily_total_label.setText("Günlük Toplam: --.-- TL")
                QtWidgets.QMessageBox.information(None, "Başarılı", "Tüm kazanç verileri sıfırlandı!")
                
            except Exception as e:
                QtWidgets.QMessageBox.warning(None, "Hata", f"Veriler sıfırlanırken bir hata oluştu: {str(e)}")

    def get_frame(self):
        return self.earnings_frame 