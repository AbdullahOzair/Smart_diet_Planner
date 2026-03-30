import re

def analyze_views(filepath):
    print(f"--- Analyzing {filepath} ---")
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    elifs = re.findall(r'\{%\s*elif\s+view\s*==', text)
    print('Number of elifs for view:', len(elifs))

    ifs = re.findall(r'\{%\s*if\s+view\s*==', text)
    print('Number of ifs for view:', len(ifs))

analyze_views('flask_app/templates/user_dashboard.html.bak')
