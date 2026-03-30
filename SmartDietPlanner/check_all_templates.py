import os
import re
import sys
sys.path.insert(0, './flask_app')
from app import app

views = list(app.view_functions.keys())

missing = set()
for root, dirs, files in os.walk('flask_app/templates'):
    for file in files:
        if file.endswith('.html'):
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                content = f.read()
                matches = re.findall(r"url_for\('([^']+)'", content)
                matches += re.findall(r'url_for\("([^"]+)"', content)
                for m in matches:
                    if m not in views and m != 'static':
                        missing.add(m)

print("Missing views:", missing)
