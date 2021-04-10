"""Initialization postgresql database for oanda data"""

 

class InitDB:
    """  Initialization for different data base"""
    def __init__(self):
        self.db = None
        self.id_field = None
        account = Account(oanda_auth_keys[1], oanda_auth_keys[1]['id'])
        print(account)
        self.instruments = account.get_instruments_names()

        print('Found instruments:')
        print(self.instruments)
        print(f'Count of instruments: {len(self.instruments)}')

    def psql_init(self):
        self.db = PSQLConn('oanda')
        self.id_field = 'id SERIAL PRIMARY KEY'
        self.__create_table__()
        self.db.conn.commit()

    def sqlite_init(self):
        self.db = SQLiteConn("DB/oanda.sqlite")
        self.id_field = 'id INTEGER PRIMARY KEY'
        self.__create_table__()
        self.db.commit()

    def __create_table__(self):
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


if __name__ == "__main__":
    init = InitDB()
    """Use the following arguments to initialize the Database during start 
        psql, sqlite ...
        default is psql
    """
    if len(sys.argv) == 1 or sys.argv[1] == 'psql':
        init.psql_init()
    elif sys.argv[1] == 'sqlite':
        init.sqlite_init()
    else:
        print('wrong argument!')
 ql   del init
