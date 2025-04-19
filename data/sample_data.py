import sqlite3
from pathlib import Path
import requests
import os
from dotenv import load_dotenv  # Импортируем для работы с .env

# Загружаем переменные из .env
load_dotenv()

DB_PATH = Path(__file__).parent / "movies.db"
OMDB_API_KEY = os.getenv("OMDB_API_KEY")  # Получаем ключ из переменных окружения


def create_database():
    """Создание базы данных с тестовыми данными"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Создание таблиц
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        year INTEGER,
        genre TEXT,
        rating REAL,
        director TEXT,
        description TEXT,
        imdb_id TEXT,
        UNIQUE(imdb_id)  # Убедимся, что IMDB ID уникален
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER,
        status TEXT CHECK(status IN ('watched', 'planned', 'watching', 'dropped')),
        user_rating INTEGER,
        FOREIGN KEY (movie_id) REFERENCES movies (id)
    )
    """)

    conn.commit()
    conn.close()


def fetch_movie_from_omdb(title, year=None):
    """Получение данных о фильме с OMDB API"""
    if not OMDB_API_KEY:
        raise ValueError("OMDB API ключ не найден. Проверьте файл .env")

    base_url = "http://www.omdbapi.com/"
    params = {
        "t": title,
        "apikey": OMDB_API_KEY,
        "plot": "full",
        "r": "json"
    }

    if year:
        params["y"] = year

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "True":
            return {
                "title": data.get("Title"),
                "year": int(data.get("Year", "0").split("–")[0]),
                "genre": data.get("Genre"),
                "rating": float(data.get("imdbRating", 0)),
                "director": data.get("Director"),
                "description": data.get("Plot"),
                "imdb_id": data.get("imdbID")
            }
        else:
            print(f"Фильм не найден: {title} ({year}) - {data.get('Error')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к OMDB API: {e}")
        return None


def add_movie_from_online(title, year=None):
    """Добавление фильма из OMDB в базу данных"""
    movie_data = fetch_movie_from_omdb(title, year)

    if not movie_data:
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT OR IGNORE INTO movies 
        (title, year, genre, rating, director, description, imdb_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            movie_data["title"],
            movie_data["year"],
            movie_data["genre"],
            movie_data["rating"],
            movie_data["director"],
            movie_data["description"],
            movie_data["imdb_id"]
        ))

        conn.commit()
        print(f"Фильм '{movie_data['title']}' успешно добавлен в базу данных")
        return True

    except sqlite3.Error as e:
        print(f"Ошибка при добавлении в базу данных: {e}")
        return False

    finally:
        conn.close()


if __name__ == "__main__":
    # Создаем БД если ее нет
    create_database()

    # Пример добавления фильмов
    movies_to_add = [
        ("The Shawshank Redemption", 1994),
        ("Inception", 2010),
        ("Pulp Fiction", 1994),
        ("The Dark Knight", 2008)
    ]

    for title, year in movies_to_add:
        add_movie_from_online(title, year)

    print("Операции завершены.")