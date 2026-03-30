#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flask_app'))

from flask_app.app import get_user_profile_for_template

print("Testing get_user_profile_for_template function...")
try:
    result = get_user_profile_for_template(2)
    if result:
        print(f"[OK] Function returned data: {len(result)} fields")
        print(f" First name: {result[3]}")
        print(f"Last name: {result[4]}")
    else:
        print("[WARNING] Function returned None")
except Exception as e:
    print(f"[ERROR] Function failed: {e}")
    import traceback
    traceback.print_exc()
