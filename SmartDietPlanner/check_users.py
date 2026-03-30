#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flask_app'))

from flask_app.db import execute_query

# Check if any users exist
result = execute_query("SELECT user_id, username, email FROM USERS LIMIT 10")
if result:
    print("Users in database:")
    for row in result:
        print(f"  ID: {row[0]}, Username: {row[1]}, Email: {row[2]}")
else:
    print("❌ No users in database!")
    print("\nCreating a test user...")
    
    # Create a test user
    try:
        from datetime import datetime
        query = """
            INSERT INTO USERS (username, email, password_hash, first_name, last_name,
                             date_of_birth, gender, weight, height, activity_level,
                             created_date, units_preference)
            VALUES (:username, :email, :password, :first_name, :last_name,
                    :dob, :gender, :weight, :height, :activity_level,
                    :created, :units)
        """
        params = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'test123',
            'first_name': 'Test', 
            'last_name': 'User',
            'dob': '1995-05-15',
            'gender': 'Male',
            'weight': 75,
            'height': 180,
            'activity_level': 'Moderate',
            'created': datetime.now(),
            'units': 'Metric'
        }
        execute_query(query, params)
        print("✓ Test user created!")
        
        # Get the users again
        result = execute_query("SELECT user_id, username FROM USERS LIMIT 1")
        if result:
            print(f"✓ New user ID: {result[0][0]}")
    except Exception as e:
        print(f"Error creating user: {e}")
