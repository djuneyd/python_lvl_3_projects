import sqlite3
con = sqlite3.connect("First_SQL\youtube.db") # подключается если есть и создаёт если нету.

cur = con.cursor() # для взаимодействия с бд.

# создаёт таблицу ЕСЛИ её нету в файле бд.
cur.execute('CREATE TABLE IF NOT EXISTS youtube (id INTEGER, name TEXT NOT NULL, link TEXT NOT NULL, author TEXT, release_date TEXT, description TEXT)')

videos = [(5, "рецепт пельменей" , "ютуб/рикролл", "бабушка нюся", "01/12/2002", "очень вкусно"), 
          (10, "пять ночей с фредди" , "ютуб/оаоаоаоа", "про хакер 228", "04/04/2024", "очень страшна"),
          (456, "я позвонил в мчс в 3 часа ночи" , "ютуб/психушка/точка/ком", "ваня эксперементатор", "66/66/1999", "я в больничке"),
          (1488, "бравл старс на тостере" , "ютуб/игры", "шампанское", "12/12/1212", "тостер сгорел..."),
          (1, "первое видиво" , "ютуб/олды", "петя", "01/01/1", "что такое ютуб?")
          ]

cur.executemany("INSERT INTO youtube VALUES(?,?,?,?,?,?)", videos) # добавление данных.

cur.execute('UPDATE youtube SET id=10 WHERE name="рецепт пельменей"') # апдейт записи.
cur.execute('DELETE FROM youtube WHERE id > 10') # удаление записей.

for row in cur.execute('SELECT * FROM youtube'):
    print(row)

con.commit() # сохранить изменения.
con.close() # Закрыть соединение с БД.