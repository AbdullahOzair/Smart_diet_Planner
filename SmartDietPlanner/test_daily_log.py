#!/usr/bin/env python3
"""Test daily log insertion"""
import sys
sys.path.insert(0, 'flask_app')
import os
os.chdir(r'd:\7th semester\merge semester project\Smart_diet_Planner\SmartDietPlanner')

from db import execute_query

# Test inserting a daily log entry
user_id = 2  # testuser_direct
log_date = '2026-03-26'  # Today
calories_consumed = 2000
calories_burned = 500
water_intake = 8
sleep_hours = 7
weight = 70.5
notes = 'Test daily log entry'

query = """
    INSERT INTO DAILY_LOG 
    (user_id, log_date, total_calories_consumed, total_calories_burned, 
     water_intake, sleep_hours, weight, notes)
    VALUES (%(user_id)s, TO_DATE(%(log_date)s, 'YYYY-MM-DD'), 
            %(calories_consumed)s, %(calories_burned)s, 
            %(water_intake)s, %(sleep_hours)s, %(weight)s, %(notes)s)
"""

params = {
    'user_id': user_id,
    'log_date': log_date,
    'calories_consumed': calories_consumed,
    'calories_burned': calories_burned,
    'water_intake': water_intake,
    'sleep_hours': sleep_hours,
    'weight': weight,
    'notes': notes
}

print("=" * 60)
print("Testing DAILY_LOG insertion...")
print("=" * 60)
print(f"Query: {query}\n")
print(f"Params: {params}\n")

result = execute_query(query, params, fetch=False)
print(f"Result: {result}")

if result:
    print("✓ Daily log inserted successfully!")
    
    # Verify by reading it back
    print("\nVerifying by reading back...")
    verify_query = "SELECT * FROM DAILY_LOG WHERE user_id = %(user_id)s AND log_date = TO_DATE(%(log_date)s, 'YYYY-MM-DD')"
    verify_result = execute_query(verify_query, {'user_id': user_id, 'log_date': log_date})
    
    if verify_result:
        print(f"✓ Found {len(verify_result)} log entries")
        print(f"  Log data: {verify_result[0]}")
    else:
        print("✗ Could not verify insertion")
else:
    print("✗ Daily log insertion failed")
