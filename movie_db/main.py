import sqlite3

conn = sqlite3.connect('movie_db\movie.db')
cur = conn.cursor()

cur.execute('''SELECT title FROM movies WHERE release_date < '1980' AND vote_average > 8 ORDER BY vote_count DESC LIMIT 1 ''')

result = cur.fetchall()
print(*result)