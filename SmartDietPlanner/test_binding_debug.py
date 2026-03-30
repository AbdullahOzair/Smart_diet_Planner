#!/usr/bin/env python3
"""Quick parameter binding test"""
import sys
import os
os.chdir(r'd:\7th semester\merge semester project\Smart_diet_Planner\SmartDietPlanner')
sys.path.insert(0, 'flask_app')

from db import execute_query, _to_pg

# Test the parameter conversion
query_template = 'SELECT user_id, username FROM USERS WHERE user_id = %(user_id)s'
params = {'user_id': 2}
converted_query, converted_params = _to_pg(query_template, params)
print("Original query:", query_template)
print("Converted query:", converted_query)
print("Original params:", params)
print("Converted params:", converted_params)
print()

# Now run the actual query
print("Executing query with parameter binding...")
result = execute_query(query_template, params)
print(f"Result: {result}")
