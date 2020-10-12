import sqlite3
from databases import DataBases


class SQLiteConn(sqlite3.Connection, DataBases):  # The class expands the possibilities of working with the database

    def __init__(self, db_file):
        super().__init__(db_file)
        self.cur = self.cursor()


if __name__ == "__main__":
    print("CHECK ZONE")
    db_path = 'DB/oanda.sqlite'
    db = SQLiteConn(db_path)
    help(db.select_from_to_max)
    records = db.select_from_to_max('EUR_USD', 'timestamp', 1601485325)
    print(records)


