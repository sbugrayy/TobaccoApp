from src.database_manager import DatabaseManager

class ProductManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def get_all_products(self):
        """Tüm ürünleri veritabanından çeker."""
        return self.db_manager.read_data()

    def add_product(self, product_data):
        """Yeni bir ürün ekler."""
        products = self.db_manager.read_data()
        new_id = self.db_manager.generate_new_id(products)
        product_data["id"] = new_id
        products.append(product_data)
        return self.db_manager.write_data(products)