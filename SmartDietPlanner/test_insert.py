
from flask_app.db import execute_query
params = {
    'username': 'testuser5',
    'email': 'testuser5@test.com',
    'password': 'password123',
    'first_name': '',
    'last_name': '',
    'dob': '',
    'gender': '',
    'weight': '',
    'height': '',
    'activity_level': '',
    'dietary_preference': 'None',
    'health_condition': 'None'
}
insert_query = """
    INSERT INTO USERS (
        username, email, password_hash, first_name, last_name,
        date_of_birth, gender, weight, height, activity_level,
        dietary_preference, health_condition
    ) VALUES (
        %(username)s, %(email)s, %(password)s, %(first_name)s, %(last_name)s,
        TO_DATE(%(dob)s, 'YYYY-MM-DD'), %(gender)s, %(weight)s, %(height)s, 
        %(activity_level)s, %(dietary_preference)s, %(health_condition)s
    )
"""
ret = execute_query(insert_query, params, fetch=False)
print('RESULT:', ret)
