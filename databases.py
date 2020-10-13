import sqlite3
from decorators import try_decor
from say import Say
from abc import ABC, abstractmethod
from logger import Logger


log = Logger(__name__)
# class ConnectDB(sqlite3.Connection):  # The class expands the possibilities of working with the database
#     count = 0
#
#     def __init__(self, db_file):
#         super().__init__(db_file)
#         self.cur = self.cursor()
#         ConnectDB.count += 1
#
#     """Create table in Data base with try-exception
#     EXAMPLE IN
#         create_table('table_name',
#             '''
#                 id INTEGER PRIMARY KEY,
#                 name TEXT UNIQUE NOT NULL,
#                 url TEXT UNIQUE NOT NULL,
#                 description TEXT
#             '''
#     """


class DataBases(ABC):

    def __init__(self):
        self.cur = None

    @try_decor
    def create_table(self, table, fields):
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table} ({fields})")
        Say(f"Created the table: {table}").prn_ok()
        return True

    @try_decor
    def select_all(self, table):
        self.cur.execute(f"SELECT * FROM {table}")
        records = self.cur.fetchall()
        Say(f"Got records: {len(records)}").prn_ok()
        return records

    @try_decor
    def select_max(self, table, max_field):
        self.cur.execute(f"SELECT MAX({max_field}) FROM {table}")
        return self.cur.fetchall()[0][0]

    @try_decor
    def select_from_to_max(self, table, field, from_value) -> list:
        """
        Select all field records from DB with from value of 'field' to max value
        :param table: string: DB Table Name
        :param field: string: Field for data select
        :param from_value: int or float: Value of field for Select from which to
        :return:  List of Tuples: DB Records
        """
        self.cur.execute(f"SELECT * FROM {table} WHERE {field} >= {from_value}")
        return self.cur.fetchall()


    @try_decor
    def insert(self, table, data_obj):
        """
        Insert to table in Data Base from object to one record
        :param table: string: DB Table Name
        :param data_obj: obj: Data for insertField for data select
        :param from_value: int or float: Value of field for Select from which to
        :return int: last id of new DB record
        :example
            insert('table_name',
               [{
                "login": "test_login",
                "password": "test_passwd",
                "id_service": 1,
                "id_person": None
                },
                {
                "login": "test_login",
                "password": "test_passwd",
                "id_service": 2,
                "id_person": None
                },
                ...
                ]
        """
        fields = ''
        values = []
        binds = '?, ' * (len(data_obj[0]) - 1) + '?'
        for key, value in data_obj.items():
            fields += f'{key}, '
            values.append(value)
        fields = fields.rstrip(", ")
        query = f'INSERT OR IGNORE INTO {table} ({fields}) VALUES ({binds})'
        return self.cur.execute(query, values).lastrowid


if __name__ == "__main__":
    print("CHECK ZONE")
    db_path = 'DB/oanda.sqlite'
    conn = ConnectDB(db_path)
    help(conn.select_from_to_max)
    records = conn.select_from_to_max('EUR_USD', 'timestamp', 1601485325)
    print(records)


