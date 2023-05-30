import psycopg2

ENDPOINT="database-3.cjxdo8ioz7b5.us-east-1.rds.amazonaws.com"
PORT="5432"
USER="postgres"
PORT='5432'

def connect():
    connection = psycopg2.connect(
        database="postgres",
        user=USER,
        password="RjT12899!",
        host=ENDPOINT,
        port=PORT
    )
    cursor=connection.cursor()
    return cursor, connection

def close(cursor, connection):
    cursor.close()
    connection.close()