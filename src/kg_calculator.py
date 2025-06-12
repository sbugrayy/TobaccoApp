class KgCalculator:
    KG_TO_GRAM_FACTOR = 1000

    @staticmethod
    def calculate_price_from_grams(kg_price, grams):
        """
        Belirli bir kilogram fiyatı ve gram miktarı için toplam fiyatı hesaplar.
        kg_price: 1 kg ürünün fiyatı (TL)
        grams: Hesaplamak istenen gram miktarı
        """
        if kg_price <= 0:
            raise ZeroDivisionError("Kilogram fiyatı sıfır veya negatif olamaz.")
        if grams < 0:
            raise ValueError("Gram miktarı negatif olamaz.")
        price_per_gram = kg_price / KgCalculator.KG_TO_GRAM_FACTOR
        return price_per_gram * grams

    @staticmethod
    def calculate_grams_from_price(kg_price, desired_price):
        """
        Belirli bir kilogram fiyatı ve istenen toplam fiyat için kaç gram alınabileceğini hesaplar.
        kg_price: 1 kg ürünün fiyatı (TL)
        desired_price: İstenen toplam fiyat (TL)
        """
        if kg_price <= 0:
            raise ZeroDivisionError("Kilogram fiyatı sıfır veya negatif olamaz.")
        if desired_price < 0:
            raise ValueError("İstenen fiyat negatif olamaz.")
        grams_per_tl = KgCalculator.KG_TO_GRAM_FACTOR / kg_price
        return grams_per_tl * desired_price