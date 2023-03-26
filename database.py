import os
import sqlite3

import argon2
from fastapi import HTTPException

from logger import logger


class Database:

    def connection(self):
        logger.info("Opening database connection to " +
                    os.path.abspath("database.db") + "...")
        conn = sqlite3.connect("database.db", isolation_level=None)
        conn.execute("PRAGMA JOURNAL_MODE=WAL")
        return conn

    def run_query(self, query, **kwargs):
        try:
            conn = self.connection()
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
            conn.close()

    def encrypt(self, password):
        return argon2.PasswordHasher().hash(password)

    def verify_password(self, password, hashed):
        return argon2.PasswordHasher().verify(hashed, password)

    def __init__(self):
        self.run_query(
            "CREATE TABLE IF NOT EXISTS admins (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)")
        self.run_query(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)")
        self.run_query("CREATE TABLE IF NOT EXISTS salt (salt TEXT)")

        if self.run_query("SELECT * FROM admins") == []:
            self.run_query("INSERT INTO admins (username, password) VALUES (:username, :password)",
                           username="admin", password=self.encrypt("admin"))


db = Database()
