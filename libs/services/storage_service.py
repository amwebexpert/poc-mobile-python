import logging
from typing import List
from kivymd.app import MDApp
import sqlite3
import os

SEP = ", "


class StorageService:
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.conn = None
        self.cursor = None


    def connect(self) -> None:
        self.conn = sqlite3.connect(f"{MDApp.get_running_app().user_data_dir}/{self.db_name}")
        self.cursor = self.conn.cursor()

    def close(self) -> None:
        self.conn.close()

    def execute(self, query: str, params: List[any] = None) -> None:
        if params is None:
            params = []
        logging.debug("sqlite: %s", query)
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except sqlite3.Error as error:
            self.raise_exception(query, error)
            self.conn.rollback()

    def fetchall(self, query: str) -> List[tuple]:
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as error:
            self.raise_exception(query, error)
            return []

    def fetchone(self, query: str) -> tuple:
        try:
            self.cursor.execute(query)
            return self.cursor.fetchone()
        except sqlite3.Error as error:
            self.raise_exception(query, error)
            return None

    def create_table(self, table_name: str, columns: tuple) -> None:
        if not columns:
            raise ValueError("Must provide at least one column")
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({SEP.join(columns)})"
        self.execute(query)

    def insert(self, table_name: str, columns: tuple, values: tuple) -> int:
        self.validate_array_lengths(columns, values)
        query = f"INSERT INTO {table_name} ({SEP.join(columns)}) VALUES ({self.build_placeholders(values)})"
        self.execute(query, values)
        return self.cursor.lastrowid

    def update(self, table_name: str, columns: tuple, values: tuple, condition: str) -> None:
        self.validate_array_lengths(columns, values)
        query = f"UPDATE {table_name} SET {SEP.join(columns)} = {self.build_placeholders(values)} WHERE {condition}"
        self.execute(query, values)

    def delete(self, table_name: str, condition: str) -> None:
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.execute(query)
        if self.cursor.rowcount == 0:
            logging.warning('No rows deleted for query: "%s"', query)

    def select(self, table_name, columns: tuple, condition: str = "1=1"):
        query = f"SELECT {SEP.join(columns)} FROM {table_name} WHERE {condition}"
        return self.fetchall(query)

    def raise_exception(self, query: str, error: sqlite3.Error) -> None:
        error_message = f'Error while executing query "{query}": {error}'
        logging.critical(error_message, stack_info=True)
        raise RuntimeError(error_message)

    def validate_array_lengths(self, columns: tuple, values: tuple):
        if len(columns) != len(values):
            raise ValueError(
                f"columns count: {len(columns)} != values count: {len(values)}")

    def build_placeholders(self, values: tuple) -> str:
        return ("?, " * len(values)).rstrip(", ")
