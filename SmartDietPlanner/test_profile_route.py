#!/usr/bin/env python3
"""Test profile endpoint"""
import sys
sys.path.insert(0, 'flask_app')
import os
os.chdir(r'd:\7th semester\merge semester project\Smart_diet_Planner\SmartDietPlanner')

from app import app
from flask import session

# Create test client
client = app.test_client()

# Test 1: Access profile without login
print("=" * 60)
print("TEST 1: Access profile without login")
print("=" * 60)
response = client.get('/user/profile')
print(f"Status code: {response.status_code}")
print(f"Location header: {response.location if response.status_code in [301, 302] else 'N/A'}")

# Test 2: Try to access with a session
print("\n" + "=" * 60)
print("TEST 2: Simulate logged-in user")
print("=" * 60)
with client.session_transaction() as sess:
    sess['user_id'] = 2
    sess['username'] = 'testuser_direct'
    sess['first_name'] = 'Test'

response = client.get('/user/profile')
print(f"Status code: {response.status_code}")
print(f"Response length: {len(response.data)} bytes")

# Check if profile data is in the response
if b'testuser' in response.data:
    print("✓ Profile data found in response")
else:
    print("✗ Profile data NOT found in response")

# Check for specific profile fields
if b'My Complete Profile' in response.data:
    print("✓ Profile page heading found")
else:
    print("✗ Profile page heading NOT found")
