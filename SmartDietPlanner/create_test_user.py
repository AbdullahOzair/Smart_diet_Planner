"""Create a test user for login"""
import psycopg2
import os

conn = psycopg2.connect(
    host=os.getenv('PG_HOST', 'localhost'),
    port=os.getenv('PG_PORT', '5432'),
    database=os.getenv('PG_DATABASE', 'smart_diet_planner'),
    user=os.getenv('PG_USER', 'postgres'),
    password=os.getenv('PG_PASSWORD', 'postgres')
)
cursor = conn.cursor()

# Create test user
try:
    cursor.execute("""
        INSERT INTO USERS (username, email, password_hash, first_name, last_name,
                          gender, date_of_birth, weight, height, activity_level)
        VALUES ('testuser', 'test@email.com', 'test123', 'Test', 'User',
                'Male', '1995-01-01'::date, 75.0, 175.0, 'Moderate')
    """)
    conn.commit()
    print("✅ Test user created!")
    print("Username: testuser")
    print("Password: test123")
except Exception as e:
    conn.rollback()
    print(f"User may already exist or error: {e}")

cursor.close()
conn.close()
