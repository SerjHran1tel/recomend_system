from dataclasses import dataclass
from typing import Optional

@dataclass
class Movie:
    """Класс для представления фильма"""
    id: int
    title: str
    year: int
    genre: str
    rating: float
    director: str
    description: Optional[str] = None

@dataclass
class UserMovie:
    """Класс для представления фильма пользователя"""
    id: int
    movie_id: int
    status: str  # 'watched', 'planned', 'watching', 'dropped'
    user_rating: Optional[int] = None