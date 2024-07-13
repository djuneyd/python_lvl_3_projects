import sqlite3

conn = sqlite3.connect('movie_db\movie.db')
cur = conn.cursor()

cur.execute('SELECT * FROM movies')

result = cur.fetchall()

# Вывод результатов
for row in result:
    print(row)
conn.close()