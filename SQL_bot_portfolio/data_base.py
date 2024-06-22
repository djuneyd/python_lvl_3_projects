import sqlite3
from config import *


class DB_Manager:
    def __init__(self, database):
        self.database = database # имя базы данных
        
    def create_tables(self):
        con = sqlite3.connect(f"SQL_bot_portfolio/{self.database}")
        
        with con:
            con.execute('''CREATE TABLE IF NOT EXISTS projects (project_id INTEGER PRIMARY KEY,
                                    user_id INTEGER,
                                    project_name TEXT NOT NULL,
                                    description TEXT,
                                    url TEXT,
                                    status_id INTEGER,
                                    FOREIGN KEY (status_id) REFERENCES status(status_id))''')
            
            con.execute('''CREATE TABLE IF NOT EXISTS project_skills (skill_id INTEGER,
                            project_id INTEGER,
                            FOREIGN KEY(skill_id) REFERENCES skills(skill_id),
                            FOREIGN KEY(project_id) REFERENCES projects(project_id))''')

            con.execute('''CREATE TABLE IF NOT EXISTS status (status_id INTEGER PRINARY KEY,
                                status_name TEXT)''')

            con.execute('''CREATE TABLE IF NOT EXISTS skills (skill_id INTEGER PRIMARY KEY,
                            skill_name TEXT)''')
            con.commit()

if __name__ == '__main__':
    db = DB_Manager(DATABASE)
    db.create_tables()