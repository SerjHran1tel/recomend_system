import subprocess
import sys
from pathlib import Path

def create_conda_env():
    """Создание виртуальной среды conda"""
    env_name = "movie_recommender_env"
    try:
        subprocess.run(["conda", "create", "--name", env_name, "--file", "requirements.txt", "-y"], check=True)
        print(f"Среда {env_name} успешно создана.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании среды: {e}")
        sys.exit(1)

def install_dependencies():
    """Установка зависимостей"""
    try:
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        print("Зависимости успешно установлены.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при установке зависимостей: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Настройка приложения Movie Recommender...")
    create_conda_env()
    install_dependencies()
    print("Настройка завершена. Активируйте среду и запустите main.py")