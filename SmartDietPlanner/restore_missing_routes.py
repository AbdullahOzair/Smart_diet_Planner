import re

f1 = 'flask_app/templates/user_dashboard.html'
with open(f1, 'r', encoding='utf-8') as f:
    text = f.read()

endpoints = set()
for match in re.finditer(r'url_for\(["\']([^"\']+)["\']', text):
    endpoints.add(match.group(1))

print("Endpoints found:", endpoints)

# Check which ones are defined in app.py
with open('flask_app/app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

missing = []
for ep in endpoints:
    if ep != 'static' and not re.search(r'def\s+' + ep + r'\s*\(', app_code):
        missing.append(ep)

print("Missing in app.py:", missing)

if missing:
    addition = "\n# --- Recovered missing routes ---\n"
    for m in missing:
        addition += f'''\n@app.route('/user/{m.replace("_", "-")}')\ndef {m}():\n    return render_template('user_dashboard.html', view='{m}')\n'''
    
    with open('flask_app/app.py', 'a', encoding='utf-8') as f:
        f.write(addition)
    print("Added these to the end of app.py to avoid BuildErrors")
