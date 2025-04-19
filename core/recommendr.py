from typing import List, Dict
from core.database import Database


class Recommender:
    """Класс для генерации рекомендаций"""

    def __init__(self):
        self.db = Database()

    def get_recommendations(self, limit: int = 10) -> List[Dict]:
        """Получить персональные рекомендации"""
        # Получаем просмотренные фильмы пользователя
        watched_movies = self.db.get_user_movies("watched")

        if not watched_movies:
            # Если нет просмотренных фильмов, рекомендуем популярные
            return self._get_popular_recommendations(limit)

        # Получаем любимые жанры пользователя
        favorite_genres = self._get_favorite_genres(watched_movies)

        # Получаем рекомендации по жанрам
        recommendations = []
        for genre in favorite_genres:
            movies = self.db.get_movies_by_genre(genre)
            for movie in movies:
                if not self._is_movie_watched(movie['id'], watched_movies):
                    movie['reason'] = f"Похоже на ваши любимые фильмы в жанре {genre}"
                    recommendations.append(movie)

        # Убираем дубликаты и сортируем по рейтингу
        unique_recs = {m['id']: m for m in recommendations}.values()
        sorted_recs = sorted(unique_recs, key=lambda x: x['rating'], reverse=True)

        return list(sorted_recs)[:limit]

    def _get_popular_recommendations(self, limit: int) -> List[Dict]:
        """Получить популярные рекомендации (по умолчанию)"""
        movies = self.db.get_top_movies(limit)
        for movie in movies:
            movie['reason'] = "Популярный фильм с высоким рейтингом"
        return movies

    def _get_favorite_genres(self, movies: List[Dict]) -> List[str]:
        """Определить любимые жанры пользователя"""
        genre_counts = {}

        for movie in movies:
            if movie['genre']:
                for genre in movie['genre'].split(', '):
                    genre = genre.strip()
                    genre_counts[genre] = genre_counts.get(genre, 0) + 1

        # Сортируем жанры по частоте встречаемости
        sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)

        # Возвращаем топ-3 жанра
        return [genre for genre, count in sorted_genres[:3]]

    def _is_movie_watched(self, movie_id: int, watched_movies: List[Dict]) -> bool:
        """Проверить, просмотрен ли фильм"""
        return any(m['id'] == movie_id for m in watched_movies)