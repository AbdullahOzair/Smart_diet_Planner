#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flask_app'))

from flask_app.app import app

with app.test_client() as client:
    # Simulate logged-in user
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    
    response = client.get('/user/profile')
    print(f'Status Code: {response.status_code}')
    
    if response.status_code != 200:
        html = response.data.decode('utf-8', errors='ignore')
        # Print first 2000 chars to see the error
        print("Response preview:")
        print(html[%(2000)s])
    else:
        print("✓ Profile route works successfully")
        html = response.data.decode('utf-8', errors='ignore')
        # Check if profile variable is in the HTML
        if "'/profile'" in html or "profile[" in html:
            print("✓ Profile variable found in HTML")
        else:
            print("✗ Profile variable NOT found in HTML")
