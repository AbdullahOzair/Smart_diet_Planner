import sys
sys.path.insert(0, './flask_app')
import db
rows = db.execute_query('SELECT user_id, weight, height FROM users LIMIT 3')
print('User DB data:', rows)
