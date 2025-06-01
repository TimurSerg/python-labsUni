import sqlite3
import hashlib

DATABASE_NAME = 'user_accounts.db'

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
    except sqlite3.Error as e:
        print(f"Помилка підключення\     до БД: {e}")
    return conn

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL
            );
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Помилка при створенні таблиці: {e}")

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def add_user(conn, login, password, full_name):
    password_hash = hash_password(password)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (login, password_hash, full_name)
            VALUES (?, ?, ?)
        """, (login, password_hash, full_name))
        conn.commit()
        print(f"Користувача '{login}' успішно додано.")
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        print(f"Помилка: Користувач з логіном '{login}' вже існує.")
    except sqlite3.Error as e:
        print(f"Помилка при додаванні користувача: {e}")
    return None

def update_password(conn, login, new_password):
    new_password_hash = hash_password(new_password)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET password_hash = ?
            WHERE login = ?
        """, (new_password_hash, login))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Пароль для користувача '{login}' успішно оновлено.")
        else:
            print(f"Користувача з логіном '{login}' не знайдено.")
    except sqlite3.Error as e:
        print(f"Помилка при оновленні пароля: {e}")

def check_authentication(conn, login, password_attempt):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT password_hash FROM users WHERE login = ?
        """, (login,))
        record = cursor.fetchone()

        if record:
            stored_password_hash = record[0]
            attempted_password_hash = hash_password(password_attempt)
            if stored_password_hash == attempted_password_hash:
                print(f"Автентифікація для '{login}' успішна. Ласкаво просимо, {get_user_fullname(conn, login)}!")
                return True
            else:
                print(f"Невірний пароль для користувача '{login}'.")
                return False
        else:
            print(f"Користувача з логіном '{login}' не знайдено.")
            return False
    except sqlite3.Error as e:
        print(f"Помилка при перевірці автентифікації: {e}")
        return False

def get_user_fullname(conn, login):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT full_name FROM users WHERE login = ?", (login,))
        record = cursor.fetchone()
        if record:
            return record[0]
    except sqlite3.Error as e:
        print(f"Помилка отримання повного імені: {e}")
    return ""


if __name__ == '__main__':
    conn = create_connection()

    if conn:
        create_table(conn)

        while True:
            print("\nОберіть дію:")
            print("1. Додати нового користувача")
            print("2. Оновити пароль користувача")
            print("3. Перевірити автентифікацію")
            print("4. Вийти")

            choice = input("Ваш вибір: ")

            if choice == '1':
                login = input("Введіть логін: ")
                password = input("Введіть пароль: ")
                full_name = input("Введіть повне ПІБ: ")
                add_user(conn, login, password, full_name)
            elif choice == '2':
                login = input("Введіть логін користувача, якому потрібно оновити пароль: ")
                new_password = input("Введіть новий пароль: ")
                update_password(conn, login, new_password)
            elif choice == '3':
                login = input("Введіть логін для автентифікації: ")
                password_attempt = input("Введіть пароль: ")
                check_authentication(conn, login, password_attempt)
            elif choice == '4':
                print("Вихід з програми.")
                break
            else:
                print("Невірний вибір. Спробуйте ще раз.")

        conn.close()