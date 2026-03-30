"""Test database connection and profile query"""
import sys
sys.path.insert(0, 'd:\\7th semester\\merge semester project\\Smart_diet_Planner\\SmartDietPlanner\\flask_app')

from db import execute_query

# Test 1: Simple connection test
print("=" * 60)
print("TEST 1: Simple connection test")
print("=" * 60)
query = "SELECT 1"
result = execute_query(query)
print(f"Result: {result}")

# Test 2: Check users table
print("\n" + "=" * 60)
print("TEST 2: Check USERS table exists")
print("=" * 60)
query = "SELECT COUNT(*) FROM USERS"
result = execute_query(query)
print(f"Result: {result}")
if result:
    print(f"Number of users: {result[0][0]}")

# Test 3: Get first user
print("\n" + "=" * 60)
print("TEST 3: Get first user (all columns)")
print("=" * 60)
query = "SELECT * FROM USERS LIMIT 1"
result = execute_query(query)
print(f"Result: {result}")
if result:
    print(f"First user columns: {len(result[0])}")

# Test 4: Get specific user profile
print("\n" + "=" * 60)
print("TEST 4: Get user profile for user_id 1")
print("=" * 60)
query = """
    SELECT user_id, username, email, first_name, last_name,
           TO_CHAR(date_of_birth, 'YYYY-MM-DD') as dob,
           gender, weight, height, activity_level, 
           dietary_preference, health_condition,
           TO_CHAR(created_date, 'YYYY-MM-DD') as created,
           country, units_preference, target_weight, goal, allergies,
           fitness_goal_speed, cooking_preference, daily_water_goal, sleep_hours
    FROM USERS 
    WHERE user_id = %(user_id)s
"""
result = execute_query(query, {'user_id': 1})
print(f"Result: {result}")
if result:
    print(f"Profile data: {result[0]}")
    print(f"Number of columns: {len(result[0])}")
