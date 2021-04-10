import psycopg2


db_name = "oanda"

#establishing the connection
conn = psycopg2.connect(
   database="postgres", user='postgres', password='password', host='127.0.0.1', port= '5432'
)
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Preparing query to create a database
sql = f'CREATE database {db_name}';

#Creating a database
cursor.execute(sql)
print("Database created successfully...")

#Closing the connection
conn.close()
