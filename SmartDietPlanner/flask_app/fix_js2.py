import re

with open('templates/user_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'function addWaterGlass\(\) \{.*?(?=\n\s*console\.log\(`[^`]*?Water progress: )', text, re.DOTALL)
if m:
    print('Found broken block!', len(m.group(0)))
    text = text.replace(m.group(0), '')
    with open('templates/user_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(text)
else:
    print("Not found")

# Run through node to verify syntax
