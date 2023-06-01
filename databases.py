import sqlite3
from sqlite3 import Error


class Database:

    def __init__(self, db_file: str = None):
        if db_file is None:
            self.db_file = "database.db"
        self.conn = self._create_connection(self.db_file)

    def _create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

    def create_table(self, create_table_sql):
        try:
            print("I try to create table")
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(f"error: {e}")

    def write_payment(self, payment):
        sql = ''' INSERT INTO payments (money, name, category, date) VALUES(?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, payment)
        self.conn.commit()
        return cur.lastrowid
