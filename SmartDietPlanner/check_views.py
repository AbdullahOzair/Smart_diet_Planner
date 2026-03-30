import re
with open('flask_app/templates/user_dashboard.html.bak', 'r', encoding='utf-8') as f:
    content = f.read()

# Try elif as well
views = re.findall(r'\{%\s*(?:if|elif)\s+view\s*==\s*[\'"]([^\'"]+)[\'"]\s*%\}', content)
print('Backup views found:', views)

try:
    m = re.search(r'\{%\s*if\s+view\s*==\s*[\'"]dashboard[\'"]\s*%\}(.*?)\{%\s*(?:elif|else|endif)', content, re.DOTALL)
    if m:
        print('dashboard length:', len(m.group(1)))
        print(m.group(1)[:200])
    else:
        print("dashboard block not found or empty")
except Exception as e:
    print(e)
