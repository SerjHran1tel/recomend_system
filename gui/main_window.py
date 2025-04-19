from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
)
from PyQt5.QtCore import Qt
from gui.top_movies import TopMoviesWindow
from gui.recommendations import RecommendationsWindow
from gui.movie_library import MovieLibraryWindow


class MainWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowTitle("Movie Recommender")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Заголовок
        title = QLabel("Добро пожаловать в Movie Recommender!")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 30px;")
        layout.addWidget(title)

        # Кнопки меню
        buttons = [
            ("Топ фильмы по жанрам", self.show_top_movies),
            ("Подборка фильмов", self.show_recommendations),
            ("Фильмотека", self.show_movie_library)
        ]

        for text, callback in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet(self.get_button_style())
            btn.clicked.connect(callback)
            layout.addWidget(btn)

    def get_button_style(self):
        """Возвращает стиль кнопки из конфига"""
        primary_color = self.config.get('colors', {}).get('primary', '#2c3e50')
        return f"""
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border: none;
                padding: 10px;
                font-size: 16px;
                margin: 5px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #1a2636;
            }}
        """

    def show_top_movies(self):
        """Показать окно топовых фильмов"""
        self.top_movies_window = TopMoviesWindow(self.config)
        self.top_movies_window.show()

    def show_recommendations(self):
        """Показать окно рекомендаций"""
        self.recommendations_window = RecommendationsWindow(self.config)
        self.recommendations_window.show()

    def show_movie_library(self):
        """Показать окно фильмотеки"""
        self.movie_library_window = MovieLibraryWindow(self.config)
        self.movie_library_window.show()