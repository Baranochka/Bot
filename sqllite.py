import sqlite3

def create():
    # Создание подключения к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Создание таблицы users с полями chat_id и password
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            user_name TEXT,
            val_orig_calls INTEGER
        )
    ''')

    # Сохранение изменений и закрытие соединения с базой данных
    conn.commit()
    conn.close()

def read():
    # Создание подключения к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Выборка всех записей из таблицы users
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()

    # Вывод содержимого таблицы
    for row in rows:
        print(row)

    # Закрытие соединения с базой данных
    conn.close()
def delete_all_records():
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для удаления всех записей
    cursor.execute("DELETE FROM users")  # Замените 'table_name' на имя вашей таблицы

    # Сохраняем изменения и закрываем соединение с базой данных
    conn.commit()
    conn.close()

# Пример использования

# delete_all_records()
# create()
read()