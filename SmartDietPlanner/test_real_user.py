#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flask_app'))

from flask_app.app import app

with app.test_client() as client:
    # Simulate logged-in user with ID 2 (testuser_direct)
    with client.session_transaction() as sess:
        sess['user_id'] = 2
    
    response = client.get('/user/profile')
    print(f'Status Code: {response.status_code}')
    
    if response.status_code != 200:
        html = response.data.decode('utf-8', errors='ignore')
        print("ERROR RESPONSE:")
        print(html[%(3000)s])
    else:
        print("✓ Profile route returned 200")
        html = response.data.decode('utf-8', errors='ignore')
        
        # Check for Jinja errors
        if 'UndefinedError' in html or 'undefined' in html.lower() or 'jinja2' in html.lower():
            print("\n⚠️  ERROR in template rendering:")
            # Find the error in the HTML
            start = html.find('Error')
            if start != -1:
                print(html[max(0, start-200)%(start)s+1000])
        elif 'profile[' in html:
            print("✓ Profile array found in HTML")
        else:
            print("✓ Profile variable not used directly in array format")
        
        # Look for the edit buttons
        if 'onclick="editProfileSection' in html:
            print("✓ Edit buttons found in HTML")
        else:
            print("✗ Edit buttons NOT found")
