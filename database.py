import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    # This one line replaces dbname, user, password, host, and port
    # It pulls the entire string from Render
    conn_string = os.getenv("DATABASE_URL")
    
    try:
        return psycopg.connect(conn_string)
    except psycopg.Error as e:
        print("Error connecting:", e)
        return None