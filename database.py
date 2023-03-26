import queue
import argon2

from fastapi import HTTPException
from logger import logger
import sqlite3


class Database:
    MAX_POOL_SIZE = 10

    def __init__(self):
        self._connection_pool = queue.Queue(maxsize=self.MAX_POOL_SIZE)
        self.run_query(
            "CREATE TABLE IF NOT EXISTS admins (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)")
        self.run_query(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)")
        self.run_query("CREATE TABLE IF NOT EXISTS salt (salt TEXT)")

        if self.run_query("SELECT * FROM admins") == []:
            self.run_query("INSERT INTO admins (username, password) VALUES (:username, :password)",
                           username="admin", password=self.encrypt("admin"))

    def _create_connection(self):
        conn = sqlite3.connect("database.db", isolation_level=None)
        conn.execute("PRAGMA JOURNAL_MODE=WAL")
        return conn

    def _get_connection(self):
        try:
            conn = self._connection_pool.get_nowait()
        except queue.Empty:
            conn = self._create_connection()
        return conn

    def _release_connection(self, conn):
        try:
            self._connection_pool.put_nowait(conn)
        except queue.Full:
            conn.close()

    def encrypt(self, password):
        return argon2.PasswordHasher().hash(password)

    def verify_password(self, password, hashed):
        return argon2.PasswordHasher().verify(hashed, password)

    def run_query(self, query, **kwargs):
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            logger.debug("QUERY: %s", query)
            cursor.execute(query, kwargs)
            conn.commit()
            result = cursor.fetchall()
            return result
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            cursor.close()
            self._release_connection(conn)


db = Database()
