"""Initialization postgresql database"""
import psycopg2
from account import Account
from security import oanda_auth_keys


print('oanda_auth_keys[1]', oanda_auth_keys[1])
account = Account(oanda_auth_keys[1], oanda_auth_keys[1]['id'])
instruments = account.get_instruments_names()
print('Found instruments:')
print(instruments)
print(f'Count of instruments: {len(instruments)}')


conn = psycopg2.connect(
    host="localhost",
    database="oanda",
    user="postgres",
    password="")

print(conn)
cur = conn.cursor()

# execute a statement
print('PostgreSQL database version:')
cur.execute('SELECT version()')

# display the PostgreSQL database server version
db_version = cur.fetchone()
print(db_version)

# for instrument in instruments:
#     conn.create_table(instrument,
#                       '''id INTEGER PRIMARY KEY,
#                          timestamp INTEGER UNIQUE NOT NULL,
#                          bid_high REAL NOT NULL,
#                          bid_low REAL NOT NULL,
#                          bid_open REAL NOT NULL,
#                          bid_close REAL NOT NULL,
#                          ask_high REAL NOT NULL,
#                          ask_low REAL NOT NULL,
#                          ask_open REAL NOT NULL,
#                          ask_close REAL NOT NULL,
#                          volume REAL NOT NULL
#                       ''')

# close the communication with the PostgreSQL
cur.close()