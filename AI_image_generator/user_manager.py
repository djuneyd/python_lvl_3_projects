from config import *
import sqlite3

class User_manager:
    def __init__(self, database):
        self.database = database

    def create_user_table(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users 
                                (id INTEGER PRIMARY KEY, 
                                telegram_id INTEGER UNIQUE, 
                                username TEXT)''')
            conn.commit()

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    
    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
        
    def get_users_telegram_id(self):
        sql = "SELECT telegram_id FROM users"
        return self.__select_data(sql)
    
    def add_user(self, telegram_id, username):
        sql = "INSERT INTO users (telegram_id, username) VALUES (?,?)"
        self.__executemany(sql, [(telegram_id, username)])

    
if __name__ == "__main__":
    user_manager = User_manager(DATABASE)
    user_manager.create_user_table()