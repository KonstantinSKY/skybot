import sqlite3
from decorators import try_decor
from say import Say


class ConnectDB(sqlite3.Connection):  # The class expands the possibilities of working with the database
    count = 0

    def __init__(self, db_file):
        super().__init__(db_file)
        self.cur = self.cursor()
        ConnectDB.count += 1

    """Create table in Data base with try-exception
    EXAMPLE IN
        create_table('table_name',
            '''
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                url TEXT UNIQUE NOT NULL,
                description TEXT
            ''' 
    """

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

    """Insert to table in Data base with try-exception
    EXAMPLE IN
        insert('table_name',
           {
            "login": "test_login",
            "password": "test_passwd",
            "id_service": 1,
            "id_person": None
        }   
    """

    @try_decor
    def insert(self, table, data_obj):
        fields = ''
        values = []
        binds = '?, ' * (len(data_obj[0]) - 1) + '?'
        for key, value in data_obj.items():
            fields += f'{key}, '
            values.append(value)
        fields = fields.rstrip(", ")
        query = f'INSERT OR IGNORE INTO {table} ({fields}) VALUES ({binds})'
        return self.cur.execute(query, values).lastrowid

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

