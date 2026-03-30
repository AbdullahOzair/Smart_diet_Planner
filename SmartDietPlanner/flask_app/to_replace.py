def user_add_goal():
    """User add new goal"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        goal_type = request.form.get('goal_type')
        target_value = request.form.get('target_value')
        current_value = request.form.get('current_value')
        target_date = request.form.get('target_date')

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

        try:
            if execute_query(query, params, fetch=False):
                flash('Goal created successfully!', 'success')
                return redirect(url_for('user_goals'))
            else:
                flash('Failed to create goal', 'error')
        except Exception as e:
            flash(f'Error creating goal: {str(e)}', 'error')

    profile = execute_query("SELECT weight FROM USERS WHERE user_id = %(u)s", {'u': user_id})
    current_weight = float(profile[0][0]) if profile and profile[0][0] else 0.0

    return render_template('user_dashboard.html', view='add_goal', current_weight=current_weight)