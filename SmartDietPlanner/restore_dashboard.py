import re

with open('flask_app/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

func = """
@app.route('/user/dashboard')
def user_dashboard():
    \"\"\"User dashboard - main view\"\"\"
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']

    # Get user statistics
    stats = {
        'total_logs': 0,
        'total_meals': 0,
        'total_activities': 0,
        'active_goals': 0
    }

    # Count daily logs
    result = execute_query("SELECT COUNT(*) FROM DAILY_LOG WHERE user_id = %(user_id)s", {'user_id': user_id})
    if result:
        stats['total_logs'] = result[0][0]

    # Count meal logs (through DAILY_LOG since MEAL_LOG has no user_id)
    result = execute_query(\"\"\"
        SELECT COUNT(*) FROM MEAL_LOG ml
        JOIN DAILY_LOG d ON ml.daily_log_id = d.daily_log_id
        WHERE d.user_id = %(user_id)s
    \"\"\", {'user_id': user_id})
    if result:
        stats['total_meals'] = result[0][0]

    # Count activity logs
    result = execute_query(\"\"\"
        SELECT COUNT(*) FROM ACTIVITY_LOG al
        JOIN DAILY_LOG d ON al.daily_log_id = d.daily_log_id
        WHERE d.user_id = %(user_id)s
    \"\"\", {'user_id': user_id})
    if result:
        stats['total_activities'] = result[0][0]

    # Count active goals
    result = execute_query("SELECT COUNT(*) FROM GOALS WHERE user_id = %(user_id)s AND status = 'Active'", {'user_id': user_id})
    if result:
        stats['active_goals'] = result[0][0]

    today_log_q = execute_query("SELECT water_intake FROM DAILY_LOG WHERE user_id = %(u)s AND DATE(log_date) = CURRENT_DATE", {'u': user_id})
    today_water = today_log_q[0][0] if today_log_q and today_log_q[0][0] is not None else 0
    today_tracking = {'water': today_water, 'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0, 'fiber': 0, 'steps': 0, 'cal_burned': 0, 'calories_consumed': 0, 'calories_burned': 0}
    user_prof = execute_query("SELECT * FROM USERS WHERE user_id = %(u)s", {'u': user_id})
    
    return render_template('user_dashboard.html', stats=stats, today_tracking=today_tracking, user_profile=user_prof[0] if user_prof else [])
"""

if 'def user_dashboard():' not in text:
    text = text.replace('@app.route(\'/user/profile\')', func + '\n@app.route(\'/user/profile\')')
    with open('flask_app/app.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Injected user_dashboard()")
