import sqlite3
from pathlib import Path
from typing import List, Dict

DB_PATH = Path(__file__).parent.parent / "data" / "movies.db"


class Database:
    """Класс для работы с базой данных"""

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        self.conn.close()

    def get_all_genres(self) -> List[str]:
        """Получить все уникальные жанры"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT genre FROM movies")
        genres = set()

        for row in cursor.fetchall():
            if row['genre']:
                for genre in row['genre'].split(', '):
                    genres.add(genre.strip())

        return sorted(genres)

    def get_top_movies(self, limit: int = 50) -> List[Dict]:
        """Получить топ фильмов по рейтингу"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM movies 
            ORDER BY rating DESC 
            LIMIT ?
        """, (limit,))

        return [dict(row) for row in cursor.fetchall()]

    def get_movies_by_genre(self, genre: str) -> List[Dict]:
        """Получить фильмы по жанру"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM movies 
            WHERE genre LIKE ? 
            ORDER BY rating DESC
        """, (f"%{genre}%",))

        return [dict(row) for row in cursor.fetchall()]

    def get_user_stats(self) -> Dict[str, int]:
        """Получить статистику пользователя"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM user_movies 
            GROUP BY status
        """)

        stats = {'watched': 0, 'planned': 0, 'watching': 0, 'dropped': 0}
        for row in cursor.fetchall():
            stats[row['status']] = row['count']

        return stats

    def get_user_movies(self, status: str) -> List[Dict]:
        """Получить фильмы пользователя по статусу"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT m.*, um.user_rating 
            FROM movies m
            JOIN user_movies um ON m.id = um.movie_id
            WHERE um.status = ?
            ORDER BY m.rating DESC
        """, (status,))

        return [dict(row) for row in cursor.fetchall()]

    def add_movie_to_library(self, movie_id: int, status: str, user_rating: int = None):
        """Добавить фильм в фильмотеку пользователя"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO user_movies (movie_id, status, user_rating)
            VALUES (?, ?, ?)
        """, (movie_id, status, user_rating))
        self.conn.commit()