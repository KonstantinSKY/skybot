import psycopg2
from psycopg2 import extras
from databases import DataBases
from decorators import try_decor



class PSQLConn(DataBases):

    def __init__(self, db_name):
        super().__init__()
        self.conn = psycopg2.connect(
            host="localhost",
            database=db_name,
            user="postgres",
            password="")
        self.cur = self.conn.cursor()
        self.extras = psycopg2.extras

    @try_decor
    def insert_many(self, table, data_obj, conflict_field):
        fields = ''
        fields_list = []
        #binds = '?, ' * (len(data_obj[0])-1) + '?'

        for key in data_obj[0]:
            fields += f'{key}, '
            fields_list.append(key)


        fields = fields.rstrip(", ")
        print(fields)
        values = [tuple(item[field] for field in fields_list) for item in data_obj]
        print(values[0])
        # query = f'''INSERT INTO {table} ({fields}) VALUES ({binds}) ON CONFLICT ({conflict_field}) DO NOTHING'''
        query = f'''INSERT INTO {table} ({fields}) VALUES %s ON CONFLICT ({conflict_field}) DO NOTHING'''
        self.extras.execute_values(self.cur, query, values, template=None,  page_size=5000)
        print(query)
        #print(values)
        #self.cur.executemany(query, values)



if __name__ == '__main__':
    db = PSQLConn('oanda')
    # db.create_table('table_name',
    #         '''
    #             id INTEGER PRIMARY KEY,
    #             name TEXT UNIQUE NOT NULL,
    #             url TEXT UNIQUE NOT NULL,
    #             description TEXT
    #         ''')
    db.conn.commit()

    db.cur.execute(f"SELECT * FROM table_name")
    records = db.cur.fetchall()
    print(f"Got records: {len(records)}")

    sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
    db.cur.execute(sql)
    tables = db.cur.fetchall()
    print(tables)
