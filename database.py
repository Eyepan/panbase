import os
import sqlite3
import uuid
import bcrypt
from fastapi import HTTPException

from logger import logger


class Database:

    def connection(self):
        # HOLY FUCK THIS TOOK ME A LONG TIME TO FIGURE OUT
        # note to self: why
        conn = sqlite3.connect(os.path.join(os.path.dirname(
            __file__), 'database.db'), isolation_level=None)
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
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(
                e).replace("table", "collection").capitalize())

    def encrypt(self, password):
        return bcrypt.hashpw(password.encode(), self.salt_value)

    def verify_password(self, password: str, hashed):
        return hashed == bcrypt.hashpw(password.encode(), self.salt_value)

    def __init__(self):
        self.run_query(
            "CREATE TABLE IF NOT EXISTS admins (id TEXT PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
        self.run_query(
            "CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
        self.run_query("CREATE TABLE IF NOT EXISTS salt (salt TEXT)")
        result = self.run_query("SELECT * FROM salt")
        if result == []:
            self.salt_value = bcrypt.gensalt()
            self.run_query("INSERT INTO salt (salt) VALUES (:salt)",
                           salt=self.salt_value)
        else:
            self.salt_value = result[0][0]
        if self.run_query("SELECT * FROM admins") == []:
            self.run_query("INSERT INTO admins (id, username, password) VALUES (:id, :username, :password)",
                           id=str(uuid.uuid4()), username="admin", password=self.encrypt("admin"))


db = Database()
