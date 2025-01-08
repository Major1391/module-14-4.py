
import sqlite3

'''CRUD = Create, Read, Update, Delete'''

def initiate_db():
    connection = sqlite3.connect('database-products-and-users.db')
    cursor = connection.cursor()

    # создаем таблицу Products в БД, если ее нет:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL,
        image TEXT NOT NULL
        )''')

    # создаем таблицу Users в БД, если ее нет:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        )''')

    # сохраняем изменения и закрываем соединение с БД:
    connection.commit()
    connection.close()

def add_user(username: str, email: str, age: int):
    '''принимает: имя пользователя, почту и возраст.
    Данная функция должна добавлять в таблицу Users вашей БД запись с переданными данными.
    Баланс у новых пользователей всегда равен 1000. Для добавления записей в таблице используйте SQL запрос.'''
    connection = sqlite3.connect('database-products-and-users.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)', (username, email.lower(), age, 1000))
    # сохраняем изменения и закрываем соединение с БД:
    connection.commit()
    connection.close()

def is_included(username):
    # принимает имя пользователя и возвращает True, если такой пользователь есть в таблице Users,
    # в противном случае False. Для получения записей используйте SQL запрос.
    connection = sqlite3.connect('database-products-and-users.db')
    cursor = connection.cursor()
    check_user = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    check_user = False if check_user.fetchone() is None else True
    connection.close()
    return check_user

def _fill_db():
    connection = sqlite3.connect('database-products-and-users.db')
    cursor = connection.cursor()
    # если пустая:
    for j in range(1, 5):
        cursor.execute('INSERT INTO Products (title, description, price, image) VALUES (?, ?, ?, ?)',
                       (f'Product-{j}', f'описание {j}', j*100, f'photo_{j}'))
    # сохраняем изменения и закрываем соединение с БД:
    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('database-products-and-users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connection.close()
    return products

def print_db():
    connection = sqlite3.connect('database-products-and-users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    col_names = [_[0] for _ in cursor.description]
    print(col_names)
    for p in products:
        print(p)
    connection.close()

if __name__ == '__main__':
    initiate_db()
    _fill_db()
    print_db()