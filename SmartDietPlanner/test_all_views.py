#!/usr/bin/env python3
"""Comprehensive test of all views"""
import sys
sys.path.insert(0, 'flask_app')
import os
os.chdir(r'd:\7th semester\merge semester project\Smart_diet_Planner\SmartDietPlanner')

from app import app

client = app.test_client()

# Set up authenticated session
with client.session_transaction() as sess:
    sess['user_id'] = 2
    sess['username'] = 'testuser_direct'
    sess['first_name'] = 'Test'

test_cases = [
    ('/user/dashboard', 'Dashboard', 'Welcome back'),
    ('/user/profile', 'Profile', 'My Complete Profile'),
    ('/user/add-daily-log', 'Add Daily Log', 'Daily Log Form'),
    ('/user/goals', 'Goals', 'My Goal'),
]

print("=" * 70)
print("COMPREHENSIVE VIEW TEST")
print("=" * 70)

for path, name, expected_text in test_cases:
    print(f"\n{name} View ({path}):")
    print("-" * 70)
    
    try:
        response = client.get(path)
        print(f"  Status: {response.status_code}", end="")
        
        if response.status_code == 200:
            print(" ✓")
            response_text = response.data.decode('utf-8', errors='ignore')
            
            if expected_text.lower() in response_text.lower():
                print(f"  Content: Found '{expected_text}' ✓")
            else:
                print(f"  Content: '{expected_text}' not found ✗")
                print(f"  Response size: {len(response.data)} bytes")
        else:
            print(f" ✗ (Expected 200)")
    except Exception as e:
        print(f"  ERROR: {str(e)[%(60)s]}...")

print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print("All core views should return status 200 and appropriate content.")
print("If any view failed, there may be additional template or routing issues.")
