import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        return psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
        )
       
    except psycopg.Error as e:
        print("error connecting:", e)
        return None




        
