#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flask_app'))

from flask_app.app import app

with app.test_client() as client:
    with client.session_transaction() as sess:
        sess['user_id'] = 2
    
    response = client.get('/user/profile', follow_redirects=True)
    html = response.data.decode('utf-8', errors='ignore')
    
    print(f"Status: {response.status_code}\n")
    
    if response.status_code != 200:
        print("Error Response (first 3000 chars):")
        print(html[%(3000)s])
        print("\n...")
        print(html[-1000:])
    else:
        print("[SUCCESS] Profile page renders without error!")
