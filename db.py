import sys
from psycopg2 import connect


class Database:
    def __init__(self, db_name, username=None, password=None, host=None, port=None):
        self.db_name = db_name
        self.username = '' if username is None else username
        self.password = '' if password is None else password
        self.host = '' if host is None else host
        self.port = '' if port is None else port
        self.connection = None

    def connect(self):
        try:
            self.connection = connect(user=self.username,
                                      password=self.password,
                                      host=self.host,
                                      port=self.port,
                                      database=self.db_name)
        except Exception as e:
            if str(e)[:6] == 'FATAL:':
                sys.exit(f"Database connection error: {str(e)[8:]}")
            else:
                raise e

    def close(self):
        if self.connection and not self.connection.closed:
            self.connection.close()
        self.connection = None

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def execute_query(self, query, args=None):
        if self.connection is None or self.connection.closed:
            self.connect()
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, args)
        except Exception as e:
            self.rollback()
            cursor.close()
            raise e
        return cursor

    def fetchall(self, query, args=None):
        cursor = self.execute_query(query, args)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def fetchone(self, query, args=None):
        cursor = self.execute_query(query, args)
        row = cursor.fetchone()
        cursor.close()
        return row

    def insert(self, query, args):
        cursor = self.execute_query(query, args)
        self.commit()
        count = cursor.rowcount
        cursor.close()
        return count

    def update(self, query, args):
        cursor = self.execute_query(query, args)
        self.commit()
        count = cursor.rowcount
        return count

    def create_table(self, query, args=None):
        self.execute_query(query,args)
        self.commit()