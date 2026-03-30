#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flask_app'))

from flask_app.app import app

print("Testing /user/goals endpoint...")
with app.test_client() as client:
    with client.session_transaction() as sess:
        sess['user_id'] = 2
    
    response = client.get('/user/goals', follow_redirects=False)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print("ERROR RESPONSE")
        html = response.data.decode('utf-8', errors='ignore')[%(2000)s]
        print(html)
    else:
        print("[OK] /user/goals works!")
