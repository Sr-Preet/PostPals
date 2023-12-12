import sqlite3

conn=sqlite3.connect('database.db')
print("connectd to database successfully")

conn.execute('CREATE TABLE IF NOT EXISTS BLOGS (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, info TEXT, category TEXT, email TEXT, uname TEXT, dateTime text)')

conn.execute('CREATE TABLE IF NOT EXISTS USERS (email TEXT PRIMARY KEY, fname TEXT, lname TEXT, contact NUMBER, password TEXT)')

conn.commit()

print("Create table successfully")

conn.close()
