import codecs

def patch_app_py():
    try:
        with open('flask_app/app.py', 'r', encoding='utf-8') as f:
            content = f.read()

        get_metrics_func = '''
def get_user_health_metrics(user_id):
    from db import execute_query
    from datetime import date
    try:
        result = execute_query("SELECT weight, height, gender, date_of_birth, activity_level FROM users WHERE user_id = %(user_id)s", {'user_id': user_id})
        if not result or not result[0]:
            return {'daily_calories': 2000, 'protein': 120, 'carbs': 300, 'fats': 70, 'bmi': 'N/A', 'bmi_status': 'Unknown', 'weight': 0, 'bmi_color': 'gray'}
        
        user_data = result[0]
        weight = float(user_data[0]) if user_data[0] else 0 # kg
        height = float(user_data[1]) if user_data[1] else 0 # cm
        gender = user_data[2] or 'Other'
        dob = user_data[3]
        
        age = 30
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            
        bmi = 0
        bmi_status = 'Unknown'
        bmi_color = 'gray'
        if weight > 0 and height > 0:
            height_m = height / 100.0
            bmi = round(weight / (height_m * height_m), 1)
            if bmi < 18.5:
                bmi_status = 'Underweight'
                bmi_color = 'yellow'
            elif bmi < 25:
                bmi_status = 'Normal'
                bmi_color = 'green'
            elif bmi < 30:
                bmi_status = 'Overweight'
                bmi_color = 'yellow'
            else:
                bmi_status = 'Obese'
                bmi_color = 'red'
                
        bmr = 2000
        if weight > 0 and height > 0 and age > 0:
            if gender == 'Male':
                bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
            else:
                bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
                
        activity_map = {'Sedentary': 1.2, 'Lightly Active': 1.375, 'Moderately Active': 1.55, 'Very Active': 1.725, 'Super Active': 1.9}
        activity = user_data[4] or 'Sedentary'
        tdee = bmr * activity_map.get(activity, 1.2)
                
        protein = round((tdee * 0.3) / 4)
        carbs = round((tdee * 0.4) / 4)
        fats = round((tdee * 0.3) / 9)
        
        return {
            'daily_calories': round(tdee),
            'protein': protein,
            'carbs': carbs,
            'fats': fats,
            'bmi': bmi if bmi > 0 else 'N/A',
            'bmi_status': bmi_status,
            'bmi_color': bmi_color,
            'weight': round(weight, 1)
        }
    except Exception as e:
        print(f"Error metrics: {e}")
        return {'daily_calories': 2000, 'protein': 120, 'carbs': 300, 'fats': 70, 'bmi': 'N/A', 'bmi_status': 'Unknown', 'weight': 0, 'bmi_color': 'gray'}

'''
        if 'def get_user_health_metrics' not in content:
            content = content.replace("app = Flask(__name__)", "app = Flask(__name__)\n\n" + get_metrics_func)

        old_ret = "return render_template('user_dashboard.html', view='dashboard', stats=stats, today_tracking={'water':0, 'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0, 'fiber': 0, 'steps': 0, 'cal_burned': 0, 'calories_consumed':0, 'calories_burned':0}, health_metrics={'daily_calories': 2000, 'protein': 120, 'carbs': 300, 'fats': 70, 'bmi': 'N/A', 'bmi_status': 'Unknown', 'weight': 60})"
        new_ret = "return render_template('user_dashboard.html', view='dashboard', stats=stats, today_tracking={'water':0, 'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0, 'fiber': 0, 'steps': 0, 'cal_burned': 0, 'calories_consumed':0, 'calories_burned':0}, health_metrics=get_user_health_metrics(user_id))"
        
        content = content.replace(old_ret, new_ret)
        
        dummy_routes = '''

@app.route('/user/add-water')
def user_add_water():
    """Stub for adding water"""
    return redirect(url_for('user_add_daily_log'))

@app.route('/user/progress')
def user_progress():
    """Stub for user progress"""
    return redirect(url_for('user_profile'))

'''
        if 'def user_add_water' not in content:
            content = content + dummy_routes

        with open('flask_app/app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Patched app.py")
    except Exception as e:
        print("Error patching app_py", e)

if __name__ == '__main__':
    patch_app_py()