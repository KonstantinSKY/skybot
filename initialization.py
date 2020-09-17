from databases import ConnectDB
from oanda import Oanda, Account
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
                         high REAL NOT NULL,
                         low REAL NOT NULL,
                         open REAL NOT NULL,
                         close REAL NOT NULL,
                         volume REAL NOT NULL
                      ''')
del conn

