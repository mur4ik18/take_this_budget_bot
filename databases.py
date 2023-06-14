import sqlite3
from sqlite3 import Error


class Database:
    """
        Class for working with sqlite database
    """

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

    def check_table(self, table) -> bool:
        """ check if a table exist -> if not return False else True"""
        try:
            cur = self.conn.cursor()
            sql = f" SELECT * FROM {table}"
            cur.execute(sql).fetchone()
            return True
        except sqlite3.OperationalError:
            return False

    def create_table(self, create_table_sql):
        """ create a table in database """
        try:
            print("I try to create table")
            c = self.conn.cursor()
            c.execute(create_table_sql)
            print("Table was created")
        except Error as e:
            print(f"error: {e}")

    def write_payment(self, id, payment) -> int:
        """ write new payments in table payments(chat_id) """
        sql = f''' INSERT INTO payments{id} (money, name, category, date)
        VALUES(?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, payment)
        self.conn.commit()
        return cur.lastrowid

    def _exist_row_or_not(self, sql) -> bool:
        """
            method which will check if row with field = * exist
            for dont create dublicates

            If exist will return True
        """
        cur = self.conn.cursor()
        reponse = cur.execute(sql)
        self.conn.commit()
        print(reponse.fetchone())
        if reponse.fetchone() is None:
            return False
        else:
            return True

    def write_new_category(self, id, name) -> bool:
        """ write new payments in a categories table """
        sql = f""" INSERT INTO categories{id} (category) VALUES(?) """
        cur = self.conn.cursor()
        # SQLite wait tuple but name is str so i add name in tuple
        if self._exist_row_or_not(f" SELECT * FROM categories{id} where category='{name}' "):
            return False
        cur.execute(sql, (name,))
        self.conn.commit()
        return True

    def get_categories(self, id) -> tuple:
        """ return all categories """
        sql = f""" SELECT * FROM categories{id}"""
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def delete_categories(self, id, name):
        """ delete category and return bool """
        sql = f" DELETE FROM categories{id} WHERE category='{name}' ;"
        if not self._exist_row_or_not(f" SELECT * FROM categories{id} where category='{name}' "):
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            print(cur)
        print(self.get_categories(id))

    def return_last_payments(self, id, period) -> tuple:
        """ return last payments like list """
        sql = f" SELECT * FROM payments{id} ORDER BY -id LIMIT {period}"
        cur = self.conn.cursor()
        reponse = cur.execute(sql).fetchall()
        return reponse

    def return_result(self, sql) -> tuple:
        """ return resultate after doing sql request what you give """
        cur = self.conn.cursor()
        return cur.execute(sql).fetchall()

    def close(self):
        self.conn.close()
        print("Database was closed")
