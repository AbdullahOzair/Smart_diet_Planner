import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_CONFIG = {
    'dbname': os.environ.get('PG_DATABASE', 'smart_diet_planner'),
    'user': os.environ.get('PG_USER', 'postgres'),
    'password': os.environ.get('PG_PASSWORD', 'zainab'),
    'host': os.environ.get('PG_HOST', 'localhost'),
    'port': os.environ.get('PG_PORT', '5000')
}

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            return self.connection
        except psycopg2.DatabaseError as e:
            print(f"Database connection error: {e}")
            return None

    def get_cursor(self):
        if not self.connection:
            self.connect()
        self.cursor = self.connection.cursor()
        return self.cursor

    def close(self):
        if self.cursor: self.cursor.close()
        if self.connection: self.connection.close()

    def commit(self):
        if self.connection: self.connection.commit()

    def rollback(self):
        if self.connection: self.connection.rollback()

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.DatabaseError as e:
        print(f"Database connection error: {e}")
        return None

def execute_query(query, params=None, fetch=True):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection: return None
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if fetch:
            return cursor.fetchall()
        else:
            connection.commit()
            return True
    except psycopg2.DatabaseError as e:
        print(f"Query execution error: {e}\nQuery: {query}\nParams: {params}")  
        if connection: connection.rollback()
        return None
    finally:
        if cursor: cursor.close()
        if connection: connection.close()
