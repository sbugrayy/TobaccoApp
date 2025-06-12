import json
import os

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self._ensure_db_file_exists()

    def _ensure_db_file_exists(self):
        """Veritabanı dosyasının ve dizininin varlığını kontrol eder, yoksa oluşturur."""
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2) # Boş bir JSON listesi olarak başlat

    def read_data(self):
        """JSON dosyasından verileri okur."""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            print(f"Hata: Veritabanı dosyası bulunamadı: {self.db_path}")
            return []
        except json.JSONDecodeError:
            print(f"Hata: Veritabanı dosyası bozuk veya geçersiz JSON formatında: {self.db_path}")
            return []
        except Exception as e:
            print(f"Veri okunurken bilinmeyen bir hata oluştu: {e}")
            return []

    def write_data(self, data):
        """Verileri JSON dosyasına yazar."""
        try:
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Veri yazılırken bir hata oluştu: {e}")
            return False

    def generate_new_id(self, data):
        """Yeni bir benzersiz ID oluşturur."""
        if not data:
            return 1
        return max(product["id"] for product in data) + 1