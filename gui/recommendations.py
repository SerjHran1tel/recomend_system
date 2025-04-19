from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton
)
from PyQt5.QtCore import Qt
from core.database import Database
from core.recommender import Recommender


class RecommendationsWindow(QWidget):
    """Окно персональных рекомендаций"""

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.db = Database()
        self.recommender = Recommender()
        self.setWindowTitle("Персональная подборка")
        self.setGeometry(200, 200, 800, 600)
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Статистика
        stats = self.db.get_user_stats()
        stats_label = QLabel(
            f"Просмотрено: {stats['watched']} | "
            f"Запланировано: {stats['planned']} | "
            f"В процессе: {stats['watching']} | "
            f"Брошено: {stats['dropped']}"
        )
        layout.addWidget(stats_label)

        # Рекомендации
        rec_label = QLabel("Рекомендуемые фильмы:")
        rec_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(rec_label)

        self.rec_list = QListWidget()
        self.rec_list.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.rec_list)

        # Кнопка назад
        back_btn = QPushButton("Назад")
        back_btn.clicked.connect(self.close)
        layout.addWidget(back_btn)

        # Загрузка рекомендаций
        self.load_recommendations()

    def load_recommendations(self):
        """Загрузка рекомендаций"""
        recommendations = self.recommender.get_recommendations()
        self.rec_list.clear()

        for movie in recommendations:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, movie['id'])

            widget = QWidget()
            widget_layout = QVBoxLayout()

            title = QLabel(f"{movie['title']} ({movie['year']}) - ★ {movie['rating']}")
            title.setStyleSheet("font-weight: bold;")

            details = QLabel(f"Жанр: {movie['genre']} | Почему рекомендовано: {movie['reason']}")
            details.setStyleSheet("color: #555;")

            widget_layout.addWidget(title)
            widget_layout.addWidget(details)
            widget.setLayout(widget_layout)

            item.setSizeHint(widget.sizeHint())
            self.rec_list.addItem(item)
            self.rec_list.setItemWidget(item, widget)