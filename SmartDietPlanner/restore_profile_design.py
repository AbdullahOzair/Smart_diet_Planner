import re

# Read both files
current_path = r'D:\7th semester\merge semester project\Smart_diet_Planner\SmartDietPlanner\flask_app\templates\user_dashboard.html'
backup_path = r'D:\7th semester\merge semester project\Smart_diet_Planner\SmartDietPlanner\flask_app\templates\user_dashboard.html.bak'

with open(current_path, 'r', encoding='utf-8') as f:
    current_html = f.read()

with open(backup_path, 'r', encoding='utf-8') as f:
    backup_html = f.read()

# Extract the full colorful profile section from backup
# Find where profile view starts and ends in backup
backup_match = re.search(r'({% if view == \'profile\' %}\n.*?{% endif %}\n\s+<!-- Goals View -->)', 
                         backup_html, re.DOTALL)

if backup_match:
    colorful_profile = backup_match.group(1)
    
    # Replace in current file - find and replace the current profile section
    current_html_new = re.sub(
        r'{% if view == \'profile\' %}\n.*?{% endif %}\n\s+<!-- Goals View -->',
        colorful_profile,
        current_html,
        flags=re.DOTALL
    )
    
    with open(current_path, 'w', encoding='utf-8') as f:
        f.write(current_html_new)
    
    print("✅ SUCCESS: Profile page restored to colorful design!")
else:
    print("❌ ERROR: Could not find profile section in backup")
