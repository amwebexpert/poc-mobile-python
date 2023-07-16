import sqlite3

SEP = ", "

class StorageService:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def execute(self, query):
        print(f"--> sqlite: {query}")
        self.cursor.execute(query)
        self.conn.commit()

    def fetchall(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetchone(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def create_table(self, table_name, columns = []):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({SEP.join(columns)})"
        self.execute(query)

    def insert(self, table_name, columns = [], values = []):
        query = f"INSERT INTO {table_name} ({SEP.join(columns)}) VALUES ({SEP.join(values)})"
        self.execute(query)
        return self.cursor.lastrowid
    
    def update(self, table_name, columns = [], values = [], condition = ""):
        query = f"UPDATE {table_name} SET {SEP.join(columns)} = {SEP.join(values)} WHERE {condition}"
        self.execute(query)

    def delete(self, table_name, condition):
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.execute(query)

    def select(self, table_name, columns = [], condition = ""):
        query = f"SELECT {SEP.join(columns)} FROM {table_name} WHERE {condition}"
        return self.fetchall(query)
