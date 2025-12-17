"""
Check available Pluggable Databases (PDBs)
"""

import oracledb

DB_CONFIG = {
    'user': 'SYSTEM',
    'password': 'system',
    'dsn': 'localhost:1521/XE'
}

def check_pdbs():
    """List all PDBs in the database"""
    connection = None
    cursor = None
    
    try:
        connection = oracledb.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("=" * 80)
        print("Checking Pluggable Databases (PDBs)")
        print("=" * 80)
        
        # Check current container
        cursor.execute("SELECT SYS_CONTEXT('USERENV', 'CON_NAME') FROM DUAL")
        current_container = cursor.fetchone()[0]
        print(f"\nCurrently connected to: {current_container}")
        
        # List all PDBs
        print("\nAll PDBs in this database:")
        print("-" * 80)
        cursor.execute("""
            SELECT pdb_name, con_id, status, open_mode 
            FROM dba_pdbs 
            ORDER BY con_id
        """)
        
        pdbs = []
        for row in cursor:
            pdbs.append(row[0])
            print(f"PDB Name: {row[0]:15} | Container ID: {row[1]} | Status: {row[2]:10} | Mode: {row[3]}")
        
        if pdbs:
            print(f"\n✓ Found {len(pdbs)} PDB(s)")
            print("\nTo connect to a PDB, use DSN format: localhost:1521/<PDB_NAME>")
        else:
            print("\n⚠ No PDBs found. You might be using XE (Express Edition) without PDBs.")
            print("In Oracle XE, the default PDB is usually XEPDB1")
        
    except oracledb.DatabaseError as e:
        print(f"\nDatabase Error: {str(e)}")
        print("\nTrying to connect to common PDB names...")
        
        # Try common PDB names
        common_pdbs = ['XEPDB1', 'ORCLPDB', 'PDB1']
        for pdb_name in common_pdbs:
            try:
                test_conn = oracledb.connect(
                    user='SYSTEM',
                    password='system',
                    dsn=f'localhost:1521/{pdb_name}'
                )
                print(f"✓ Successfully connected to PDB: {pdb_name}")
                test_conn.close()
            except:
                print(f"✗ Cannot connect to: {pdb_name}")
    
    except Exception as e:
        print(f"\nError: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    check_pdbs()
