from sqlite_conn import SQLiteConn
from account import Account
from security import oanda_auth_keys

# First program setup, create the tables in db if it not exist

db = SQLiteConn("DB/oanda.sqlite")

account = Account(oanda_auth_keys[1], oanda_auth_keys[1]['id'])

instruments = account.get_instruments_names()

print('Found instruments:')
print(instruments)
print(f'Count: {len(instruments)}')

# # execute a statement
# db.cur.execute('SELECT version()')
# db_version = db.cur.fetchone()

# display the PostgreSQL database server version
#

for instrument in instruments:
    db.create_table(instrument,
                      '''id INTEGER PRIMARY KEY,
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
db.close()
del db

