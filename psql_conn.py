import psycopg2
from databases import DataBases


class PSQLConn(DataBases):

    def __init__(self, db_name):
        super().__init__()
        self.conn = psycopg2.connect(
            host="localhost",
            database=db_name,
            user="postgres",
            password="")

        print(self.conn)
        self.cur = self.conn.cursor()
        # execute a statement
        print('PostgreSQL database version:')
        self.cur.execute('SELECT version()')
        # display the PostgreSQL database server version
        db_version = self.cur.fetchone()
        print(db_version)


if __name__ == '__main__':
    db = PSQLConn('oanda')
    db.create_table('table_name',
            '''
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                url TEXT UNIQUE NOT NULL,
                description TEXT
            ''')

    db.cur.execute(f"SELECT * FROM table_name")
    records = db.cur.fetchall()
    print(f"Got records: {len(records)}")

    sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
    db.cur.execute(sql)
    tables = db.cur.fetchall()
    print(tables)
