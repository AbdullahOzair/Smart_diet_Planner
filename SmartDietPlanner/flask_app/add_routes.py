import os

app_path = 'D:/7th semester/merge semester project/Smart_diet_Planner/SmartDietPlanner/flask_app/app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    app_text = f.read()

new_routes = """
@app.route('/api/add-water-glass', methods=['POST'])
def api_add_water_glass():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    from datetime import date
    
    # Check if a daily log exists for today
    existing = execute_query("SELECT daily_log_id, water_intake FROM DAILY_LOG WHERE user_id = %(u)s AND DATE(log_date) = CURRENT_DATE", {'u': user_id})
    
    if existing:
        current_water = float(existing[0][1] or 0)
        new_water = current_water + 1  # 1 glass
        execute_query("UPDATE DAILY_LOG SET water_intake = %(w)s WHERE daily_log_id = %(id)s", {'w': new_water, 'id': existing[0][0]}, fetch=False)
    else:
        new_water = 1
        execute_query("INSERT INTO DAILY_LOG (user_id, log_date, water_intake) VALUES (%(u)s, CURRENT_DATE, %(w)s)", {'u': user_id, 'w': new_water}, fetch=False)
        
    return jsonify({'success': True, 'message': 'Water glass added successfully', 'water_glasses': new_water})

@app.route('/api/update-water-goal', methods=['POST'])
def api_update_water_goal():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
        
    # the frontend typically sends JSON, but let's be safe
    data = request.json or {}
    water_goal = data.get('water_goal', 8)
    session['water_goal'] = water_goal
    
    return jsonify({'success': True, 'message': 'Water goal updated!'})
"""

if 'api_add_water_glass' not in app_text:
    app_text = app_text.replace("if __name__ == '__main__':", new_routes + "\nif __name__ == '__main__':")
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(app_text)
    print('Routes added!')
else:
    print('Already present!')
