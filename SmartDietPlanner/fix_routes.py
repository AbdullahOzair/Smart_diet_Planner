import re

f = r'D:\7th semester\merge semester project\Smart_diet_Planner\SmartDietPlanner\flask_app\app.py'
with open(f, 'r', encoding='utf-8') as file:
    content = file.read()

# Replace the block
bad_block = """@app.route('/user/goals')

@app.route('/user/update-goal-status/<int:goal_id>', methods=['POST'])"""

good_block = """
@app.route('/user/update-goal-status/<int:goal_id>', methods=['POST'])"""

content = content.replace(bad_block, good_block)

bad_func = """def user_goals():
    \"\"\"User view own goals\"\"\""""

good_func = """@app.route('/user/goals')
def user_goals():
    \"\"\"User view own goals\"\"\""""

content = content.replace(bad_func, good_func)

with open(f, 'w', encoding='utf-8') as file:
    file.write(content)

print("Fixed app.py and reassigned routes properly.")
