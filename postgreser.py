import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the database connection parameters from environment variables
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

def get_alerts():
    # Establish a connection to the database
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a SELECT statement to retrieve all entries from the "alerts" table
    cur.execute("SELECT * FROM alerts")

    # Fetch all the rows and print them
    rows = cur.fetchall()
    # Close the cursor and database connection
    cur.close()
    conn.close()


    return(rows)

