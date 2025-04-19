import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "movies.db"


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
        description TEXT
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

    # Добавление тестовых данных
    movies = [
        ("Крестный отец", 1972, "Криминал, Драма", 9.2, "Фрэнсис Форд Коппола",
         "Эпическая история сицилийской мафиозной семьи Корлеоне."),
        ("Побег из Шоушенка", 1994, "Драма", 9.3, "Фрэнк Дарабонт",
         "История невиновного банкира, приговоренного к пожизненному заключению."),
        ("Темный рыцарь", 2008, "Боевик, Криминал, Драма", 9.0, "Кристофер Нолан",
         "Бэтмен сталкивается с Джокером, хаотичным преступным гением."),
        # Добавьте больше фильмов по аналогии
    ]

    cursor.executemany("""
    INSERT INTO movies (title, year, genre, rating, director, description)
    VALUES (?, ?, ?, ?, ?, ?)
    """, movies)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
    print("Тестовые данные успешно добавлены в базу данных.")