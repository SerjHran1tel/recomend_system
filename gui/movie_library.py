from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QMenu
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor
from core.database import Database


class MovieLibraryWindow(QWidget):
    """Окно фильмотеки пользователя"""

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.db = Database()
        self.setWindowTitle("Моя фильмотека")
        self.setGeometry(200, 200, 800, 600)
        self.current_status = "watched"
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Панель управления
        control_panel = QHBoxLayout()

        self.status_label = QLabel("Просмотрено:")
        self.status_label.setStyleSheet("font-weight: bold;")

        # Кнопка меню статусов
        self.status_menu_btn = QPushButton("☰")
        self.status_menu_btn.setFixedWidth(40)
        self.status_menu_btn.clicked.connect(self.show_status_menu)

        control_panel.addWidget(self.status_label)
        control_panel.addWidget(self.status_menu_btn)
        control_panel.addStretch()

        layout.addLayout(control_panel)

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

    def show_status_menu(self):
        """Показать меню выбора статуса"""
        menu = QMenu()

        statuses = {
            "watched": "Просмотрено",
            "planned": "Запланировано",
            "watching": "Смотрю",
            "dropped": "Брошено"
        }

        for status, label in statuses.items():
            action = menu.addAction(label)
            action.triggered.connect(lambda _, s=status: self.change_status(s))

        menu.exec_(QCursor.pos())

    def change_status(self, status):
        """Изменение текущего статуса фильмов"""
        self.current_status = status
        status_labels = {
            "watched": "Просмотрено",
            "planned": "Запланировано",
            "watching": "Смотрю",
            "dropped": "Брошено"
        }
        self.status_label.setText(status_labels[status] + ":")
        self.load_movies()

    def load_movies(self):
        """Загрузка фильмов по текущему статусу"""
        movies = self.db.get_user_movies(self.current_status)
        self.movie_list.clear()

        for movie in movies:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, movie['id'])

            widget = QWidget()
            widget_layout = QVBoxLayout()

            title = QLabel(f"{movie['title']} ({movie['year']})")
            title.setStyleSheet("font-weight: bold;")

            details = QLabel(f"Жанр: {movie['genre']} | Рейтинг: {movie['rating']}")
            details.setStyleSheet("color: #555;")

            # Если есть пользовательский рейтинг
            if movie.get('user_rating'):
                user_rating = QLabel(f"Ваша оценка: {movie['user_rating']}/10")
                user_rating.setStyleSheet("color: #2c3e50; font-style: italic;")
                widget_layout.addWidget(user_rating)

            widget_layout.addWidget(title)
            widget_layout.addWidget(details)
            widget.setLayout(widget_layout)

            item.setSizeHint(widget.sizeHint())
            self.movie_list.addItem(item)
            self.movie_list.setItemWidget(item, widget)