import re
with open('flask_app/templates/user_dashboard.html.bak', 'r', encoding='utf-8') as f:
    text = f.read()

print("Any instances of 'dashboard' string:", text.count("'dashboard'"), text.count('"dashboard"'))
matches = re.finditer(r'\{%.*?%\}', text)
for m in matches:
    if 'view' in m.group() and '==' in m.group():
        print(m.group())

# What is the default view if it's not any of the above?
# Search for else block
else_idx = text.rfind('{% else %}')
if else_idx != -1:
    print("Found else block at", else_idx)
    
