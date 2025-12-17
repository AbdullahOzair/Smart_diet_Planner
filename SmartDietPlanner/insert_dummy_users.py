"""
Insert Dummy Users into Database
This script adds 2 test users directly into the database
"""

import oracledb
from datetime import datetime

# Database configuration - Connected to PDB (XEPDB1)
DB_CONFIG = {
    'user': 'SYSTEM',
    'password': 'system',
    'dsn': 'localhost:1521/XEPDB1'  # Changed from XE (CDB) to XEPDB1 (PDB)
}

def insert_dummy_users():
    """Insert 2 dummy users into the database"""
    connection = None
    cursor = None
    
    try:
        # Connect to database
        connection = oracledb.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("Connected to database successfully!")
        
        # Dummy User 1
        user1_data = {
            'username': 'test_user1',
            'email': 'testuser1@example.com',
            'password_hash': 'hashed_password_test1',  # In production, use proper password hashing
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'date_of_birth': datetime(1995, 3, 15),
            'gender': 'Female',
            'weight': 65.5,
            'height': 165.0,
            'activity_level': 'Moderate',
            'dietary_preference': 'Vegetarian',
            'health_condition': 'None'
        }
        
        # Dummy User 2
        user2_data = {
            'username': 'test_user2',
            'email': 'testuser2@example.com',
            'password_hash': 'hashed_password_test2',  # In production, use proper password hashing
            'first_name': 'Bob',
            'last_name': 'Smith',
            'date_of_birth': datetime(1990, 7, 22),
            'gender': 'Male',
            'weight': 80.0,
            'height': 178.0,
            'activity_level': 'Active',
            'dietary_preference': 'No restrictions',
            'health_condition': 'None'
        }
        
        # SQL Insert Statement
        insert_sql = """
        INSERT INTO USERS (
            username, email, password_hash, first_name, last_name, 
            date_of_birth, gender, weight, height, activity_level, 
            dietary_preference, health_condition
        ) VALUES (
            :username, :email, :password_hash, :first_name, :last_name,
            :date_of_birth, :gender, :weight, :height, :activity_level,
            :dietary_preference, :health_condition
        )
        """
        
        # Insert User 1
        cursor.execute(insert_sql, user1_data)
        print(f"✓ Inserted user: {user1_data['username']} ({user1_data['email']})")
        
        # Insert User 2
        cursor.execute(insert_sql, user2_data)
        print(f"✓ Inserted user: {user2_data['username']} ({user2_data['email']})")
        
        # Commit the transaction
        connection.commit()
        print("\n✓ Successfully inserted 2 dummy users into the database!")
        
        # Verify insertion
        cursor.execute("SELECT user_id, username, email, first_name, last_name FROM USERS ORDER BY created_date DESC FETCH FIRST 2 ROWS ONLY")
        print("\nRecently added users:")
        print("-" * 80)
        for row in cursor:
            print(f"ID: {row[0]}, Username: {row[1]}, Email: {row[2]}, Name: {row[3]} {row[4]}")
        
    except oracledb.DatabaseError as e:
        error = str(e)
        print(f"✗ Database Error: {error}")
        if connection:
            connection.rollback()
    
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        if connection:
            connection.rollback()
    
    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("\nDatabase connection closed.")

if __name__ == "__main__":
    print("=" * 80)
    print("Smart Diet Planner - Insert Dummy Users")
    print("=" * 80)
    insert_dummy_users()
