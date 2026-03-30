#!/usr/bin/env python
"""
Complete registration test - simulates what happens when user registers
"""

import sys
import os

# Ensure we're importing from the flask_app folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flask_app'))

from db import execute_query

def test_registration():
    print("=" * 80)
    print("REGISTRATION FLOW TEST")
    print("=" * 80)
    
    # Test data
    username = 'testuser_real'
    email = 'testuser_real@test.com'
    password = 'TestPassword123'
    first_name = 'John'
    last_name = 'Doe'
    dob = '1990-05-15'
    gender = 'Male'
    weight = '75.5'
    height = '180.0'
    activity_level = 'Active'
    dietary_preference = 'Vegetarian'
    health_condition = 'None'
    
    print("\n[1] Testing username existence check...")
    check_query = "SELECT user_id FROM USERS WHERE username = %(username)s"
    result = execute_query(check_query, {'username': username})
    if result:
        print(f"    ❌ Username '{username}' already exists!")
        return False
    print(f"    ✓ Username '{username}' is available")
    
    print("\n[2] Testing email existence check...")
    check_email = "SELECT user_id FROM USERS WHERE email = %(email)s"
    result = execute_query(check_email, {'email': email})
    if result:
        print(f"    ❌ Email '{email}' already exists!")
        return False
    print(f"    ✓ Email '{email}' is available")
    
    print("\n[3] Attempting user registration...")
    insert_query = """
        INSERT INTO USERS (
            username, email, password_hash, first_name, last_name,
            date_of_birth, gender, weight, height, activity_level,
            dietary_preference, health_condition
        ) VALUES (
            %(username)s, %(email)s, %(password)s, %(first_name)s, %(last_name)s,
            TO_DATE(%(dob)s, 'YYYY-MM-DD'), %(gender)s, %(weight)s, %(height)s, 
            %(activity_level)s, %(dietary_preference)s, %(health_condition)s
        )
    """
    
    params = {
        'username': username,
        'email': email,
        'password': password,
        'first_name': first_name,
        'last_name': last_name,
        'dob': dob,
        'gender': gender,
        'weight': weight,
        'height': height,
        'activity_level': activity_level,
        'dietary_preference': dietary_preference,
        'health_condition': health_condition
    }
    
    try:
        result = execute_query(insert_query, params, fetch=False)
        if result:
            print(f"    ✓ Registration successful!")
        else:
            print(f"    ❌ Registration failed - execute_query returned False/None")
            return False
    except Exception as e:
        print(f"    ❌ Registration error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n[4] Verifying user was created...")
    verify_query = """
        SELECT user_id, username, email, first_name, last_name, 
               gender, weight, height, activity_level, dietary_preference
        FROM USERS WHERE username = %(username)s
    """
    result = execute_query(verify_query, {'username': username})
    if result:
        user = result[0]
        print(f"    ✓ User found in database!")
        print(f"      - User ID: {user[0]}")
        print(f"      - Username: {user[1]}")
        print(f"      - Email: {user[2]}")
        print(f"      - Name: {user[3]} {user[4]}")
        print(f"      - Gender: {user[5]}")
        print(f"      - Weight: {user[6]}")
        print(f"      - Height: {user[7]}")
        print(f"      - Activity Level: {user[8]}")
        print(f"      - Dietary Preference: {user[9]}")
        return True
    else:
        print(f"    ❌ User not found after insertion!")
        return False

if __name__ == '__main__':
    success = test_registration()
    print("\n" + "=" * 80)
    if success:
        print("✓ REGISTRATION TEST PASSED - Database is working correctly!")
    else:
        print("❌ REGISTRATION TEST FAILED - There is an issue with the registration process")
    print("=" * 80)
    sys.exit(0 if success else 1)
