"""
Database Connection Module
Handles Oracle database connections using oracledb
"""

import oracledb

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
DB_CONFIG = {
    'user': 'SYSTEM',
    'password': 'system',
    'dsn': 'localhost:1521/XEPDB1'  # PDB connection
}


class Database:
    """Database connection manager"""
    
    def __init__(self):
        """Initialize database connection"""
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """
        Establish connection to Oracle database
        Returns: Connection object
        """
        try:
            self.connection = oracledb.connect(**DB_CONFIG)
            return self.connection
        except oracledb.DatabaseError as e:
            print(f"Database connection error: {e}")
            return None
    
    def get_cursor(self):
        """
        Get database cursor for executing queries
        Returns: Cursor object
        """
        if not self.connection:
            self.connect()
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def close(self):
        """Close database connection and cursor"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def commit(self):
        """Commit current transaction"""
        if self.connection:
            self.connection.commit()
    
    def rollback(self):
        """Rollback current transaction"""
        if self.connection:
            self.connection.rollback()


def get_db_connection():
    """
    Helper function to get a new database connection
    Returns: Connection object
    """
    try:
        connection = oracledb.connect(**DB_CONFIG)
        return connection
    except oracledb.DatabaseError as e:
        print(f"Database connection error: {e}")
        return None


def execute_query(query, params=None, fetch=True):
    """
    Execute a database query with automatic connection management
    
    Args:
        query: SQL query string
        params: Query parameters (optional)
        fetch: Whether to fetch results (default: True)
    
    Returns:
        Query results if fetch=True, None otherwise
    """
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if not connection:
            return None
        
        cursor = connection.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            results = cursor.fetchall()
            return results
        else:
            connection.commit()
            return True
            
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        print(f"Query execution error: {error_obj.code} - {error_obj.message}")
        print(f"Query: {query}")
        print(f"Params: {params}")
        if connection:
            connection.rollback()
        return None
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
