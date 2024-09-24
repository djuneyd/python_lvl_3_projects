import sqlite3
from config import *


class MoneyTracker:
    def __init__(self, database):
        self.database = database

    def create_table(self):
        con = sqlite3.connect(self.database)
        with con:
            con.execute('''CREATE TABLE IF NOT EXISTS user_stats
                    (id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    total_money INTEGER NOT NULL)''')
            con.commit()
            
    def __executemany(self, sql, data):
        con = sqlite3.connect(self.database)
        with con:
            con.execute(sql, data) # where data is a tuple and in sql spaces are provided
            con.commit()

    def __select_data(self, sql, data = tuple()): # where data is a tuple and in sql spaces are provided and everything besides sql is written in data
        con = sqlite3.connect(self.database)
        with con:
            cur = con.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
        
if __name__ == '__main__':
    tracker = MoneyTracker(DATABASE)
    tracker.create_table()