"""Initialization postgresql database for oanda data"""
from psql_conn import PSQLConn
from sqlite_conn import SQLiteConn
from account import Account
from security import oanda_auth_keys
import sys


class DB:

    def __init__(self, type_db):
        self.db = None
        self.id_field = None
        account = Account(oanda_auth_keys[1], oanda_auth_keys[1]['id'])
        self.instruments = account.get_instruments_names()

        print('Found instruments:')
        print(self.instruments)
        print(f'Count of instruments: {len(self.instruments)}')
        print('Got argument', sys.argv[1])
        self.psql_init()

    def psql_init(self):
        self.db = PSQLConn('oanda')
        self.id_field = 'id SERIAL PRIMARY KEY'

    def sqlite_init(self):
        self.db = SQLiteConn("DB/oanda.sqlite")
        self.id_field = 'id INTEGER PRIMARY KEY'

    def create_table(self):
        for instrument in self.instruments:
            self.db.create_table(instrument,
                            f'''{self.id_field},
                                 timestamp INTEGER UNIQUE NOT NULL,
                                 bid_high REAL NOT NULL,
                                 bid_low REAL NOT NULL,
                                 bid_open REAL NOT NULL,
                                 bid_close REAL NOT NULL,
                                 ask_high REAL NOT NULL,
                                 ask_low REAL NOT NULL,
                                 ask_open REAL NOT NULL,
                                 ask_close REAL NOT NULL,
                                 volume REAL NOT NULL
                            ''')
        self.db.conn.commit()

if len(sys.argv) == 1 or sys.argv[1] == 'psql':
else:
    print('wrong argument!')
    exit()

# close the communication with the PostgreSQL
db.cur.close()
