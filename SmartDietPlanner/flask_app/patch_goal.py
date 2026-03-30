import re

def main():
    with open('app.py', 'r', encoding='utf-8') as f:
        text = f.read()

    old_func = re.search(r'def user_add_goal\(\):[\s\S]*?return render_template\(\'user_dashboard\.html\', view=\'add_goal\', current_weight=current_weight\)', text)

    if old_func:
        new_func = '''def user_add_goal():
    """User add new or update goal"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']

    # get existing active goal
    existing = execute_query("SELECT goal_id, goal_type, target_value, current_value, TO_CHAR(target_date, 'YYYY-MM-DD') FROM GOALS WHERE user_id = %(u)s AND status = 'Active' LIMIT 1", {'u': user_id}, fetch=True)
    existing_goal = existing[0] if existing else None

    if request.method == 'POST':
        goal_type = request.form.get('goal_type')
        target_value = request.form.get('target_value')
        current_value = request.form.get('current_value')
        target_date = request.form.get('target_date')

        # Translate Muscle Building to Muscle Gain as per DB check constraint
        if goal_type == 'Muscle Building':
            goal_type = 'Muscle Gain'

        if existing_goal:
            query = """
                UPDATE GOALS
                SET goal_type = %(goal_type)s, target_value = %(target_value)s,
                    current_value = %(current_value)s, target_date = %(target_date)s::DATE
                WHERE goal_id = %(goal_id)s
            """
            params = {
                'goal_id': existing_goal[0],
                'goal_type': goal_type,
                'target_value': target_value,
                'current_value': current_value,
                'target_date': target_date
            }
            msg = 'Goal updated successfully!'
        else:
            query = """
                INSERT INTO GOALS (user_id, goal_type, target_value, current_value, target_date, start_date, status)
                VALUES (%(user_id)s, %(goal_type)s, %(target_value)s, %(current_value)s,
                        %(target_date)s::DATE, CURRENT_DATE, 'Active')
            """
            params = {
                'user_id': user_id,
                'goal_type': goal_type,
                'target_value': target_value,
                'current_value': current_value,
                'target_date': target_date
            }
            msg = 'Goal created successfully!'

        try:
            if execute_query(query, params, fetch=False):
                flash(msg, 'success')
                return redirect(url_for('user_goals'))
            else:
                flash('Failed to save goal', 'error')
        except Exception as e:
            flash(f'Error saving goal: {str(e)}', 'error')

    profile = execute_query("SELECT weight FROM USERS WHERE user_id = %(u)s", {'u': user_id})
    current_weight = float(profile[0][0]) if profile and profile[0][0] else 0.0 

    # map Muscle Gain back to Muscle Building for template
    if existing_goal and existing_goal[1] == 'Muscle Gain':
        existing_goal = list(existing_goal)
        existing_goal[1] = 'Muscle Building'

    return render_template('user_dashboard.html', view='add_goal', current_weight=current_weight, existing_goal=existing_goal)'''

        text = text.replace(old_func.group(0), new_func)
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(text)
        print('Replaced successfully')
    else:
        print('Old func not found')

if __name__ == '__main__':
    main()
