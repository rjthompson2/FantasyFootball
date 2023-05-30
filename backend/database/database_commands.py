import psycopg2
from backend.database import database


def posgresql_add(tablename, values_dict):
    cursor, connection = database.connect()
    command = """INSERT INTO {tablename}("""
    keys = values_dict.keys
    for i in len(keys):
        command += keys[i]
        if i != len(keys)-1:
            command +=","
    command += """)  VALUES("""
    values = values_dict.values
    for i in len(values):
        command += values[i]
        if i != len(values)-1:
            command +=","
    command += ");"

    cursor.execute(command)

    connection.commit()

    database.close(cursor, connection)