def get_card_stylesheet(hover=False):
    base_style = """
        QFrame#ProductCard {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
            padding: 15px;
            transition: all 0.2s ease;
        }
        QLabel#ProductName {
            font-size: 16px;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
            min-height: 40px;
            max-height: 60px;
            padding: 5px;
        }
        QLabel#ProductPrice {
            font-size: 20px;
            font-weight: bold;
            color: #007bff;
            margin-bottom: 10px;
            padding: 5px;
        }
        QLabel#ProductKgStatus {
            font-size: 13px;
            color: #666;
            font-style: italic;
            padding: 5px;
        }
        QPushButton#DeleteButton {
            background-color: #ff4444;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
            margin-top: 10px;
            transition: background-color 0.3s ease;
        }
        QPushButton#DeleteButton:hover {
            background-color: #cc0000;
            cursor: pointer;
        }
    """
    if hover:
        base_style += """
            QFrame#ProductCard {
                background-color: #e6f7ff;
                border: 1px solid #007bff;
                box-shadow: 0 4px 10px rgba(0, 123, 255, 0.2);
                transform: scale(1.03);
            }
        """
    return base_style

def get_kg_calculator_stylesheet():
    return """
        QDialog {
            background-color: #f0f2f5;
            border-radius: 10px;
        }
        QLabel {
            font-size: 16px;
            color: #333;
        }
        QLabel#KgCalculatorResult {
            font-size: 18px;
            font-weight: bold;
            color: #007bff;
            padding: 10px;
            background-color: #eaf6ff;
            border-radius: 5px;
        }
        QLineEdit#KgCalculatorInput {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 15px;
            color: #333;
        }
        QLineEdit#KgCalculatorInput:focus {
            border: 1px solid #007bff;
            background-color: #ffffff;
        }
        QPushButton#ToggleButton {
            background-color: #6c757d; /* Gri */
            color: white;
            padding: 8px 15px;
            border: none;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton#ToggleButton:hover {
            background-color: #5a6268;
        }
        QPushButton#ToggleButton:checked {
            background-color: #007bff; /* Mavi seçili */
        }
    """