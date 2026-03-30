#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flask_app'))

from flask_app.app import app

print("Testing /user/profile endpoint...")
with app.test_client() as client:
    with client.session_transaction() as sess:
        sess['user_id'] = 2
    
    try:
        response = client.get('/user/profile', follow_redirects=False)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 500:
            html = response.data.decode('utf-8', errors='ignore')
           # Try to find the actual error in the HTML
            if 'Traceback' in html:
                start = html.find('Traceback')
                print("\nTraceback found:")
                print(html[start%(start)s+2000])
            else:
                print("No traceback in HTML response")
                print(html[%(1000)s])
        elif response.status_code == 200:
            print("[SUCCESS] Profile page loaded without 500 error!")
            html = response.data.decode('utf-8', errors='ignore')
            if 'UndefinedError' in html or 'profile' in html.lower() and 'undefined' in html.lower():
                print("[ISSUE] Template undefined error detected")
            else:
                print("[OK] No Template errors detected")
    except Exception as e:
        print(f"[ERROR] Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
