#!/usr/bin/env python3
# Test if app imports without error
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flask_app'))

try:
    from flask_app.app import app
    print("[OK] App imports successfully")
    print("[OK] No syntax or import errors")
except Exception as e:
    print(f"[ERROR] Exception during import: {e}")
    import traceback
    traceback.print_exc()
