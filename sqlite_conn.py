import sqlite3
from databases import DataBases
from decorators import try_decor


class SQLiteConn(sqlite3.Connection, DataBases):  # The class expands the possibilities of working with the database

    def __init__(self, db_file):
        super().__init__(db_file)
        self.cur = self.cursor()

    @try_decor
    def insert_many(self, table, data_obj):
        fields = ''
        fields_list = []
        binds = '?, ' * (len(data_obj[0])-1) + '?'

        for key in data_obj[0]:
            fields += f'{key}, '
            fields_list.append(key)

        fields = fields.rstrip(", ")
        values = [tuple(item[field] for field in fields_list) for item in data_obj]
        query = f'INSERT OR IGNORE INTO {table} ({fields}) VALUES ({binds})'
        self.cur.executemany(query, values)


if __name__ == "__main__":
    print("CHECK ZONE")
    db_path = 'DB/oanda.sqlite'
    db = SQLiteConn(db_path)
    help(db.select_from_to_max)
    records = db.select_from_to_max('EUR_USD', 'timestamp', 1601485325)
    print(records)


