"""Initialization postgresql database for oanda data"""
from psql_conn import PSQLConn
from account import Account
from security import oanda_auth_keys

db = PSQLConn('oanda')

account = Account(oanda_auth_keys[1], oanda_auth_keys[1]['id'])

instruments = account.get_instruments_names()

print('Found instruments:')
print(instruments)
print(f'Count of instruments: {len(instruments)}')

# execute a statement
db.cur.execute('SELECT version()')
db_version = db.cur.fetchone()

# display the PostgreSQL database server version
print(f'PostgreSQL database version: {db_version}')

for instrument in instruments:
    db.create_table(instrument,
                    '''id SERIAL PRIMARY KEY,
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
db.conn.commit()

# close the communication with the PostgreSQL
db.cur.close()
