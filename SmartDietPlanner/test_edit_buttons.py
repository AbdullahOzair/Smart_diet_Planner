#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flask_app'))

from flask_app.app import app

with app.test_client() as client:
    with client.session_transaction() as sess:
        sess['user_id'] = 2
    
    try:
        response = client.get('/user/profile')
        html = response.data.decode('utf-8', errors='ignore')
        
        print(f'Status: {response.status_code}')
        
        # Check for common errors
        if 'UndefinedError' in html:
            print("ERROR: UndefinedError found")
            idx = html.find('UndefinedError')
            print(html[max(0, idx-500)%(idx)s+500])
        elif 'onclick="editProfileSection' in html:
            count = html.count('onclick="editProfileSection')
            print(f"✓ SUCCESS: Found {count} edit buttons")
            print("✓ Profile page renders correctly!")
        else:
            print("⚠️  No edit buttons found (check if they use different structure)")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
