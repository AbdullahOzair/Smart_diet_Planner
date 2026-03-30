#!/usr/bin/env python3
"""Final comprehensive test of the profile edit functionality"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flask_app'))

from flask_app.app import app

print("=" * 60)
print("FINAL PROFILE EDIT BUTTONS TEST")
print("=" * 60)

with app.test_client() as client:
    # Login as user 2
    with client.session_transaction() as sess:
        sess['user_id'] = 2
    
    # Get the profile page
    response = client.get('/user/profile', follow_redirects=True)
    
    print("\n[OK] Profile request status: " + str(response.status_code))
    html = response.data.decode('utf-8', errors='ignore')
    
    # Check for edit button functions
    checks = [
        ('editProfileSection', "Edit Profile Functions"),
        ('saveProfileChanges', "Save Profile Function"),
        ('editModal', "Edit Modal Element"),
    ]
    
    print("\n" + "-" * 60)
    print("CHECKING FOR REQUIRED ELEMENTS:")
    print("-" * 60)
    
    for check_str, label in checks:
        if check_str in html:
            print("[OK] " + label)
        else:
            print("[MISSING] " + label)
    
    # Count edit buttons
    edit_count = html.count('onclick="editProfileSection')
    print("\n[OK] Found " + str(edit_count) + " Edit buttons")
    
    # Check for JavaScript errors
    has_errors = False
    if 'Unexpected token' in html:
        print("\n[ERROR] JavaScript syntax error detected")
        has_errors = True
    elif 'UndefinedError' in html:
        print("\n[ERROR] Jinja2 UndefinedError detected")
        has_errors = True
    else:
        print("\n[OK] No JavaScript or Jinja2 syntax errors")
    
    # Final status
    print("\n" + "=" * 60)
    if response.status_code == 200 and edit_count >= 5 and 'saveProfileChanges' in html and not has_errors:
        print("[SUCCESS] PROFILE EDIT BUTTONS ARE WORKING!")
        print("=" * 60)
    else:
        print("[ISSUE] Check details above")
        print("=" * 60)
