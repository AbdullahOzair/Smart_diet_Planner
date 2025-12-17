"""
Verify Users in Database
Check which schema contains the USERS table and list all users
"""

import oracledb

# Database configuration - Connected to PDB (XEPDB1)
DB_CONFIG = {
    'user': 'SYSTEM',
    'password': 'system',
    'dsn': 'localhost:1521/XEPDB1'  # Changed to PDB
}

def verify_users():
    """Check database for users and table information"""
    connection = None
    cursor = None
    
    try:
        # Connect to database
        connection = oracledb.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("=" * 80)
        print("Connected to Oracle Database successfully!")
        print("=" * 80)
        
        # Check which schemas have a USERS table
        print("\n1. Checking for USERS table in all schemas:")
        print("-" * 80)
        cursor.execute("""
            SELECT owner, table_name, num_rows 
            FROM all_tables 
            WHERE table_name = 'USERS'
            ORDER BY owner
        """)
        
        schemas_with_users = []
        for row in cursor:
            schemas_with_users.append(row[0])
            print(f"   Schema: {row[0]}, Table: {row[1]}, Rows: {row[2]}")
        
        if not schemas_with_users:
            print("   ⚠ No USERS table found in any schema!")
        
        # Check current schema
        print("\n2. Current schema/user:")
        print("-" * 80)
        cursor.execute("SELECT USER FROM DUAL")
        current_user = cursor.fetchone()[0]
        print(f"   Current user: {current_user}")
        
        # Try to query USERS table directly (will use current schema)
        print("\n3. Attempting to query USERS table in current schema:")
        print("-" * 80)
        try:
            cursor.execute("SELECT COUNT(*) FROM USERS")
            count = cursor.fetchone()[0]
            print(f"   ✓ Found {count} users in {current_user}.USERS table")
            
            # Show all users
            if count > 0:
                print("\n4. All users in the table:")
                print("-" * 80)
                cursor.execute("""
                    SELECT user_id, username, email, first_name, last_name, 
                           TO_CHAR(created_date, 'YYYY-MM-DD HH24:MI:SS') as created
                    FROM USERS 
                    ORDER BY user_id
                """)
                for row in cursor:
                    print(f"   ID: {row[0]:3} | Username: {row[1]:15} | Email: {row[2]:30} | Name: {row[3]} {row[4]}")
                    print(f"        Created: {row[5]}")
        except oracledb.DatabaseError as e:
            print(f"   ✗ Cannot query USERS table in current schema: {str(e)}")
        
        # Check each schema that has USERS table
        print("\n5. Checking users in each schema with USERS table:")
        print("-" * 80)
        for schema in schemas_with_users:
            try:
                cursor.execute(f'SELECT COUNT(*) FROM {schema}.USERS')
                count = cursor.fetchone()[0]
                print(f"\n   Schema: {schema}")
                print(f"   Total users: {count}")
                
                if count > 0:
                    cursor.execute(f"""
                        SELECT user_id, username, email, first_name, last_name
                        FROM {schema}.USERS 
                        ORDER BY user_id
                    """)
                    for row in cursor:
                        print(f"      - ID: {row[0]}, User: {row[1]}, Email: {row[2]}, Name: {row[3]} {row[4]}")
            except oracledb.DatabaseError as e:
                print(f"   ✗ Cannot access {schema}.USERS: {str(e)}")
        
        # List all schemas/users in the database
        print("\n6. All database users/schemas:")
        print("-" * 80)
        cursor.execute("""
            SELECT username, created, account_status 
            FROM dba_users 
            WHERE username NOT LIKE '%$%'
            ORDER BY created DESC
        """)
        for row in cursor:
            print(f"   - {row[0]:20} | Created: {row[1]} | Status: {row[2]}")
        
    except oracledb.DatabaseError as e:
        print(f"\n✗ Database Error: {str(e)}")
    
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("\n" + "=" * 80)
            print("Database connection closed.")
            print("=" * 80)

if __name__ == "__main__":
    verify_users()
