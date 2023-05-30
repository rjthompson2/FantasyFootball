import psycopg2
from backend.database import database

cursor, connection = database.connect()

cursor.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
for table in cursor.fetchall():
    print(table)

connection.commit()

database.close(cursor, connection)