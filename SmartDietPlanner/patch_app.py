import re

patch = """
@app.route('/user/update-goal-status/<int:goal_id>', methods=['POST'])
def update_user_goal_status(goal_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    execute_query("UPDATE GOALS SET status = 'Completed' WHERE goal_id = %(g)s AND user_id = %(u)s", {'g': goal_id, 'u': session['user_id']}, fetch=False)
    flash('Goal marked as completed!', 'success')
    return redirect(url_for('user_goals'))

@app.route('/user/diet')
def user_diet():
    return redirect(url_for('ai_recommendation'))

@app.route('/user/add-update-goal', methods=['POST'])
def user_add_update_goal():
    pass
"""

f = r'D:\7th semester\merge semester project\Smart_diet_Planner\SmartDietPlanner\flask_app\app.py'
with open(f, 'r', encoding='utf-8') as file:
    content = file.read()
if 'update_user_goal_status' not in content:
    content = content.replace('def user_goals():', patch + '\ndef user_goals():')
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    print('Routes added')
else:
    print('Already present')
