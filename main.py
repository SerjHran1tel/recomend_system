import sys
import json
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow


def load_config():
    """Загрузка конфигурации из файла"""
    config_path = Path(__file__).parent / "config" / "settings.json"
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Возвращаем пустой словарь, если файл не найден или поврежден


def main():
    """Точка входа в приложение"""
    app = QApplication(sys.argv)

    # Загрузка конфигурации
    config = load_config()

    # Установка стилей из конфига, если они есть
    if 'style' in config:
        app.setStyleSheet(config['style'])

    # Создание и отображение главного окна
    window = MainWindow(config)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()