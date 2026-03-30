import re

with open('D:/7th semester/merge semester project/Smart_diet_Planner/SmartDietPlanner/flask_app/app.py', 'r', encoding='utf-8') as f:
    app_text = f.read()

# Let's replace the occurrences of dummy_tracking where it gives 0 with a real query.
# Actually, the simplest patch is to intercept before `return render_template('user_dashboard.html'`
# But there are multiple route functions.

# I will write a script to replace dummy_tracking with actual tracking.
old_code_dash = """    return render_template('user_dashboard.html', view='dashboard', stats=stats, today_tracking={'water':0, 'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0, 'fiber': 0, 'steps': 0, 'cal_burned': 0, 'calories_consumed':0, 'calories_burned':0}, health_metrics=get_user_health_metrics(user_id))"""

new_code_dash = """    today_log_q = execute_query("SELECT water_intake FROM DAILY_LOG WHERE user_id = %(u)s AND DATE(log_date) = CURRENT_DATE", {'u': user_id})
    today_water = today_log_q[0][0] if today_log_q and today_log_q[0][0] is not None else 0
    today_tracking = {'water': today_water, 'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0, 'fiber': 0, 'steps': 0, 'cal_burned': 0, 'calories_consumed': 0, 'calories_burned': 0}
    user_prof = execute_query("SELECT * FROM USERS WHERE user_id = %(u)s", {'u': user_id})
    return render_template('user_dashboard.html', view='dashboard', stats=stats, today_tracking=today_tracking, health_metrics=get_user_health_metrics(user_id), user_profile=user_prof[0] if user_prof else [])"""

old_code_add_water = """    dummy_tracking={'water':0, 'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0, 'fiber': 0, 'steps': 0, 'cal_burned': 0, 'calories_consumed':0, 'calories_burned':0}
    return render_template('user_dashboard.html', view='add_water', health_metrics=get_user_health_metrics(session['user_id']), today_tracking=dummy_tracking)"""

new_code_add_water = """    today_log_q = execute_query("SELECT water_intake FROM DAILY_LOG WHERE user_id = %(u)s AND DATE(log_date) = CURRENT_DATE", {'u': session['user_id']})
    today_water = today_log_q[0][0] if today_log_q and today_log_q[0][0] is not None else 0
    dummy_tracking={'water':today_water, 'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0, 'fiber': 0, 'steps': 0, 'cal_burned': 0, 'calories_consumed':0, 'calories_burned':0}
    user_prof = execute_query("SELECT * FROM USERS WHERE user_id = %(u)s", {'u': session['user_id']})
    return render_template('user_dashboard.html', view='add_water', health_metrics=get_user_health_metrics(session['user_id']), today_tracking=dummy_tracking, user_profile=user_prof[0] if user_prof else [])"""

old_code_progress = """    dummy_tracking={'water':0, 'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0, 'fiber': 0, 'steps': 0, 'cal_burned': 0, 'calories_consumed':0, 'calories_burned':0}
    return render_template('user_dashboard.html', view='progress', health_metrics=get_user_health_metrics(session['user_id']), today_tracking=dummy_tracking)"""

new_code_progress = """    today_log_q = execute_query("SELECT water_intake FROM DAILY_LOG WHERE user_id = %(u)s AND DATE(log_date) = CURRENT_DATE", {'u': session['user_id']})
    today_water = today_log_q[0][0] if today_log_q and today_log_q[0][0] is not None else 0
    dummy_tracking={'water':today_water, 'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0, 'fiber': 0, 'steps': 0, 'cal_burned': 0, 'calories_consumed':0, 'calories_burned':0}
    user_prof = execute_query("SELECT * FROM USERS WHERE user_id = %(u)s", {'u': session['user_id']})
    return render_template('user_dashboard.html', view='progress', health_metrics=get_user_health_metrics(session['user_id']), today_tracking=dummy_tracking, user_profile=user_prof[0] if user_prof else [])"""

if old_code_dash in app_text:
    app_text = app_text.replace(old_code_dash, new_code_dash)
if old_code_add_water in app_text:
    app_text = app_text.replace(old_code_add_water, new_code_add_water)
if old_code_progress in app_text:
    app_text = app_text.replace(old_code_progress, new_code_progress)

with open('D:/7th semester/merge semester project/Smart_diet_Planner/SmartDietPlanner/flask_app/app.py', 'w', encoding='utf-8') as f:
    f.write(app_text)
print('Tracking logic replaced!')
