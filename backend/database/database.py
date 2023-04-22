import psycopg2

conn = psycopg2.connect(
    database="testdb",
    user="postgres",
    password="password",
    host="127.0.0.1",
    port="5432",
)

cursor = conn.cursor()

cursor.execute("select version()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Connection established to: ",data)

#Closing the connection
conn.close()
