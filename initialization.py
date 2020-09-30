from databases import ConnectDB
from sandbox.oanda import Account
import security

# First program setup, create the tables in db if it not exist

conn = ConnectDB("DB/oanda.sqlite")
account = Account(security.auth_key, security.account1_id)
account.get_instruments()
print('Found instruments:')
print(account.instruments)
print(f'Count: {len(account.instruments)}')

for instrument in account.instruments:
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

