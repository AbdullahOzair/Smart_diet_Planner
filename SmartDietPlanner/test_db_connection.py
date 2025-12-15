import oracledb

try:
    connection = oracledb.connect(
        user="SYSTEM",
        password="system",
        dsn="localhost:1521/XE"
    )

    print("Connected to Oracle Database successfully!")

    cursor = connection.cursor()
    cursor.execute("SELECT 'Oracle Connection OK' FROM dual")
    print(cursor.fetchone())

    cursor.close()
    connection.close()

except Exception as e:
    print("Connection failed:", e)
