import re

f = r'D:\7th semester\merge semester project\Smart_diet_Planner\SmartDietPlanner\flask_app\templates\user_dashboard.html'
with open(f, 'r', encoding='utf-8') as file:
    content = file.read()

content = re.sub(r'<button class="btn btn-outline-primary flex-grow-1" style="color:#2563EB; border-color:#2563EB;" onclick="showUpdateGoalModal(.*?)">\s*<i class="bi bi-pencil-square me-2"></i>Update Goal\s*</button>', 
                 r'<a href="{{ url_for(\'user_add_goal\') }}" class="btn btn-outline-primary flex-grow-1" style="color:#2563EB; border-color:#2563EB;">\n<i class="bi bi-pencil-square me-2"></i>Update Goal\n</a>', 
                 content, flags=re.DOTALL)

with open(f, 'w', encoding='utf-8') as file:
    file.write(content)
