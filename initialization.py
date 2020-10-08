from databases import ConnectDB
from account import Account
from security import oanda_auth_keys

# First program setup, create the tables in db if it not exist

conn = ConnectDB("DB/oanda.sqlite")
print('oanda_auth_keys[1]', oanda_auth_keys[1])
account = Account(oanda_auth_keys[1], oanda_auth_keys[1]['id'])
instruments = account.get_instruments_names()
print('Found instruments:')
print(instruments)
print(f'Count: {len(instruments)}')

for instrument in instruments:
    conn.create_table(instrument,
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
del conn

