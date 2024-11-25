import sqlite3

connection = sqlite3.connect('shop_database.db')
cursor = connection.cursor()
connection_users = sqlite3.connect('users_database.db')
cursor_users = connection_users.cursor()


def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL)
    ''')
    cursor_users.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INT NOT NULL,
    balance INTEGER NOT NULL)
    ''')
    connection.commit()
    connection_users.commit()

def get_all_products():
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    # for product in products:
    #     print(product)
    return products

def add_user(username, email, age):
    check_user = cursor_users.execute("SELECT * FROM Users WHERE username = ?", (username,))
    if check_user.fetchone() is None:
        cursor_users.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)", (f"{username}", f"{email}", f"{age}", 1000))
    connection_users.commit()

def is_included(username):
    check_user = cursor_users.execute("SELECT * FROM Users WHERE username = ?", (username,))
    if check_user.fetchone() is None:
        connection_users.commit()
        return False
    else:
        connection_users.commit()
        return True

def if_email_exists(email):
    check_email = cursor_users.execute("SELECT * FROM Users WHERE email = ?", (email,))
    if check_email.fetchone() is None:
        connection_users.commit()
        return False
    else:
        connection_users.commit()
        return True