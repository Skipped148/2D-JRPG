import os
import subprocess
import psycopg2 as pg


DB_PASS = os.getenv("INJ_PASS")

def run_game():
    #Запускает игру из файла main.py
    try:
        subprocess.run(["python", "main.py"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при запуске игры: {e}")
        return False
    except FileNotFoundError:
        print("Файл main.py не найден!")
        return False

def get_db_connection():
    #Создает и возвращает соединение с базой данных
    return pg.connect(
        user="Skipis",
        password=12345,
        host="localhost",
        port="5432",
        database='game_db'
    )

def db_login(login, password):
    #Аутентификация пользователя
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.callproc('login', (login, password))
        res = cursor.fetchone()
        
        if res and res[0]:  # Если авторизация успешна
            return run_game()
        return False
        
    except pg.Error as e:
        print(f"Ошибка базы данных при входе: {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def db_registration(login, password, nickname):
   #Регистрация нового пользователя 
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.callproc('registration', (login, password, nickname))
        res = cursor.fetchone()
        connection.commit()
        
        if res and res[0]:  # Если регистрация успешна
            return run_game()
        return False
        
    except pg.Error as e:
        print(f"Ошибка базы данных при регистрации: {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()