import oracledb

# Connect to database
conn = oracledb.connect(user='SYSTEM', password='system', dsn='localhost:1521/XEPDB1')
cursor = conn.cursor()

# Update passwords to "admin"
cursor.execute("""
    UPDATE USERS 
    SET password_hash = 'admin' 
    WHERE username IN ('zainab_moazzam', 'abdullah_ozair')
""")
conn.commit()

print("\n✓ Passwords updated to 'admin'")

# Verify the update
cursor.execute("""
    SELECT username, password_hash, user_id 
    FROM USERS 
    WHERE username IN ('zainab_moazzam', 'abdullah_ozair')
""")

print("\n" + "="*60)
print("ADMIN ACCOUNTS AFTER UPDATE:")
print("="*60)
for row in cursor:
    print(f"Username: {row[0]}")
    print(f"Password: {row[1]}")
    print(f"User ID: {row[2]}")
    print("-"*60)

cursor.close()
conn.close()
