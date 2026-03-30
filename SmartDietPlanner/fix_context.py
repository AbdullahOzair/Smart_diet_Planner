import re

with open('flask_app/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_block = """    result = execute_query("SELECT COUNT(*) FROM GOALS WHERE user_id = %(user_id)s AND status = 'Active'", {'user_id': user_id})
    if result:
        stats['active_goals'] = result[0][0]

    today_log_q = execute_query("SELECT water_intake FROM DAILY_LOG WHERE user_id = %(u)s AND DATE(log_date) = CURRENT_DATE", {'u': user_id})
    today_water = today_log_q[0][0] if today_log_q and today_log_q[0][0] is not None else 0
    today_tracking = {'water': today_water, 'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0, 'fiber': 0, 'steps': 0, 'cal_burned': 0, 'calories_consumed': 0, 'calories_burned': 0}
    user_prof = execute_query("SELECT * FROM USERS WHERE user_id = %(u)s", {'u': user_id})
    
    return render_template('user_dashboard.html', stats=stats, today_tracking=today_tracking, user_profile=user_prof[0] if user_prof else [])"""


text = re.sub(r'    result = execute_query\("SELECT COUNT\(\*\) FROM GOALS.*?\n    return render_template\(\'user_dashboard\.html\', stats=stats\)', new_block, text, flags=re.DOTALL)

with open('flask_app/app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Patched user_dashboard with user_profile context!")
