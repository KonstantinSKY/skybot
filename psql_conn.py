import psycopg2
from psycopg2 import extras
from databases import DataBases
from decorators import try_decor


class PSQLConn(DataBases):
    """ Class extended opportunity of psycopg2"""

    def __init__(self, db_name):
        """
        :param db_name: str -> Name of psql database
        """
        super().__init__()
        self.conn = psycopg2.connect(
            host="localhost",
            database=db_name,
            user="postgres",
            password="")
        self.cur = self.conn.cursor()
        self.extras = psycopg2.extras

    @try_decor
    def insert_many(self, table, data_obj, conflict_field=''):
        """
        Insert many records to psql DB with ignore exist
        :param table: str -> Table name
        :param data_obj: obj -> object of Data (fields: values)
        :param conflict_field: -> unique  field for check exist record for ignore
        :return: None
        """

        fields = ''
        fields_list = []

        for key in data_obj[0]:
            fields += f'{key}, '
            fields_list.append(key)

        fields = fields.rstrip(", ")

        values = [tuple(item[field] for field in fields_list) for item in data_obj]
        query = f'''INSERT INTO {table} ({fields}) VALUES %s ON CONFLICT ({conflict_field}) DO NOTHING'''
        self.extras.execute_values(self.cur, query, values, template=None,  page_size=5000)


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
