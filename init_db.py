import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO entry (title, content) VALUES (?, ?)",
    ('First entry', 'Hello world, here is my first journal entry.')
            )

cur.execute("INSERT INTO entry (title, content) VALUES (?, ?)",
    ('Second entry', 'Hello there, surely there is a better way to write entries')
            )

connection.commit()
connection.close()
