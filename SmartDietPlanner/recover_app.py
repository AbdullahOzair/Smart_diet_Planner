import os
import glob
import time

appdata = os.environ.get('APPDATA')
history_dir = os.path.join(appdata, 'Code', 'User', 'History')

candidate_files = []
print("Searching in", history_dir)
for root, _, files in os.walk(history_dir):
    for f in files:
        if f == 'entries.json': continue
        try:
            path = os.path.join(root, f)
            size = os.path.getsize(path)
            # app.py should be around 45k-55k
            if 45000 < size < 60000:
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    if 'def user_dashboard():' in content and 'app.route' in content:
                        candidate_files.append((path, os.path.getmtime(path), size))
        except:
            pass

candidate_files.sort(key=lambda x: x[1], reverse=True)
print(f"Found {len(candidate_files)} candidates")
for c in candidate_files[:5]:
    from datetime import datetime
    print(f"{c[0]}: Size={c[2]}, Time={datetime.fromtimestamp(c[1]).strftime('%Y-%m-%d %H:%M:%S')}")
