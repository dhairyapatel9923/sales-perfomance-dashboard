import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="SalesDB@8426",
        database="sales_dashboard"
    )

    if connection.is_connected():
        print("SUCCESS: Connected to MySQL and sales_dashboard!")

except mysql.connector.Error as error:
    print("ERROR:", error)

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed.")