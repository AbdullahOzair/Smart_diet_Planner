with open('flask_app/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

correct_select = "SELECT user_id, username, email, first_name, last_name, TO_CHAR(date_of_birth, 'YYYY-MM-DD') as dob, gender, weight, height, activity_level, dietary_preference, health_condition, TO_CHAR(created_date, 'YYYY-MM-DD') as created, country, units_preference, target_weight, goal, allergies, fitness_goal_speed, cooking_preference, daily_water_goal, sleep_hours FROM USERS WHERE user_id = %(u)s"

text = text.replace(
    'user_prof = execute_query("SELECT * FROM USERS WHERE user_id = %(u)s", {\'u\': user_id})',
    f'user_prof = execute_query("{correct_select}", {{\'u\': user_id}})'
)

profile_query_old = """        SELECT user_id, username, email, first_name, last_name,
               TO_CHAR(date_of_birth, 'YYYY-MM-DD') as dob,
               gender, weight, height, activity_level,
               dietary_preference, health_condition,
               TO_CHAR(created_date, 'YYYY-MM-DD') as created
        FROM USERS
        WHERE user_id = %(user_id)s"""

profile_query_new = """        SELECT user_id, username, email, first_name, last_name, TO_CHAR(date_of_birth, 'YYYY-MM-DD') as dob, gender, weight, height, activity_level, dietary_preference, health_condition, TO_CHAR(created_date, 'YYYY-MM-DD') as created, country, units_preference, target_weight, goal, allergies, fitness_goal_speed, cooking_preference, daily_water_goal, sleep_hours
        FROM USERS
        WHERE user_id = %(user_id)s"""

text = text.replace(profile_query_old, profile_query_new)

with open('flask_app/app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated queries!")