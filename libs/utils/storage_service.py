import logging
from typing import List

import sqlite3

from libs.utils.string_utils import is_blank

SEP = ", "

class StorageService:
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self) -> None:
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self) -> None:
        self.conn.close()
    
    def execute(self, query: str) -> None:
        logging.debug(f"sqlite: {query}")
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            self.raise_exception(query, e)
            self.db.rollback()    

    def fetchall(self, query: str) -> List[tuple]:
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            self.raise_exception(query, e)

    def fetchone(self, query: str) -> tuple:
        try:
            self.cursor.execute(query)
            return self.cursor.fetchone()
        except Exception as e:
            self.raise_exception(query, e)

    def create_table(self, table_name: str, columns: List[str]) -> None:
        if not columns:
            raise ValueError("Must provide at least one column")
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({SEP.join(columns)})"
        self.execute(query)

    def insert(self, table_name: str, columns: List[str], values: List[str]) -> int:
        self.validateArrayLengths(columns, values)
        query = f"INSERT INTO {table_name} ({SEP.join(columns)}) VALUES ({SEP.join(values)})"
        self.execute(query)
        return self.cursor.lastrowid
    
    def update(self, table_name: str, columns: List[str], values: List[str], condition: str) -> None:
        self.validateArrayLengths(columns, values)
        query = f"UPDATE {table_name} SET {SEP.join(columns)} = {SEP.join(values)} WHERE {condition}"
        self.execute(query)

    def delete(self, table_name: str, condition: str) -> None:
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.execute(query)
        if self.cursor.rowcount == 0:
            logging.warning(f'No rows deleted for query: "{query}"')

    def select(self, table_name, columns: List[str], condition: str = "1=1"):
        query = f"SELECT {SEP.join(columns)} FROM {table_name} WHERE {condition}"
        return self.fetchall(query)

    def raise_exception(self, query: str, e: Exception) -> None:
        raise Exception(f'Error while executing query "{query}": {e}')

    def validateArrayLengths(self, columns: List[str], values: List[str]):
        if len(columns) != len(values):
            raise ValueError(f"columns count: {len(columns)} != values count: {len(values)}")
