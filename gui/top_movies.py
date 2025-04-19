from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QListWidget, QPushButton, QListWidgetItem
)
from PyQt5.QtCore import Qt
from core.database import Database


class TopMoviesWindow(QWidget):
    """Окно топовых фильмов по жанрам"""

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.db = Database()
        self.setWindowTitle("Топ фильмы по жанрам")
        self.setGeometry(200, 200, 800, 600)
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Панель фильтров
        filter_panel = QHBoxLayout()

        genre_label = QLabel("Жанр:")
        self.genre_combo = QComboBox()
        self.genre_combo.addItem("Все жанры")
        self.genre_combo.addItems(self.db.get_all_genres())

        filter_panel.addWidget(genre_label)
        filter_panel.addWidget(self.genre_combo)
        filter_panel.addStretch()

        layout.addLayout(filter_panel)

        # Список фильмов
        self.movie_list = QListWidget()
        self.movie_list.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.movie_list)

        # Кнопка назад
        back_btn = QPushButton("Назад")
        back_btn.clicked.connect(self.close)
        layout.addWidget(back_btn)

        # Загрузка фильмов
        self.load_movies()

        # Подключение сигналов
        self.genre_combo.currentTextChanged.connect(self.load_movies)

    def load_movies(self):
        """Загрузка фильмов в список"""
        genre = self.genre_combo.currentText()
        if genre == "Все жанры":
            movies = self.db.get_top_movies()
        else:
            movies = self.db.get_movies_by_genre(genre)

        self.movie_list.clear()

        for movie in movies:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, movie['id'])

            widget = QWidget()
            widget_layout = QVBoxLayout()

            title = QLabel(f"{movie['title']} ({movie['year']}) - ★ {movie['rating']}")
            title.setStyleSheet("font-weight: bold;")

            details = QLabel(f"Жанр: {movie['genre']} | Режиссер: {movie['director']}")
            details.setStyleSheet("color: #555;")

            widget_layout.addWidget(title)
            widget_layout.addWidget(details)
            widget.setLayout(widget_layout)

            item.setSizeHint(widget.sizeHint())
            self.movie_list.addItem(item)
            self.movie_list.setItemWidget(item, widget)