import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL)
''')

# cursor.execute("INSERT INTO Users(username, email, age) VALUES (?, ?, ?) ", ('newuser', 'newuser123@gmail.com', 28))

# for i in range(10):
#     cursor.execute("INSERT INTO Users(username, email, age, balance) VALUES (?, ?, ?, ?)", (f'user{i+1}', f'example{i+1}@gmail.com', (i+1)*10, 1000))
# for i in range(1, 11, 2):
#     cursor.execute("UPDATE Users SET balance = ? WHERE username = ?", (500, f'user{i}'))

for i in range(1, 11, 3):
    cursor.execute("DELETE FROM Users WHERE username=? ", (f'user{i}',))

cursor.execute("SELECT * FROM Users WHERE age != ?", (60,))

users = cursor.fetchall()
for user in users:
    print(f'Имя: {user[1]} | Почта: {user[2]} | Возраст: {user[3]} | Баланс: {user[4]}')

connection.commit()
connection.close()
