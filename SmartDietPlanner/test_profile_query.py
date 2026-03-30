#!/usr/bin/env python3
"""Direct test of the profile query"""
import sys
import os
os.chdir(r'd:\7th semester\merge semester project\Smart_diet_Planner\SmartDietPlanner')
sys.path.insert(0, 'flask_app')

from db import execute_query

# Use one of the actual user IDs from the database
user_id = 2  # testuser_direct

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

print("Testing profile query with user_id = 2")
print("=" * 80)
result = execute_query(query, {'user_id': user_id})
print(f"Result: {result}")
if result:
    print(f"Profile retrieved: {result[0]}")
else:
    print("ERROR: No profile retrieved!")
