"""Test parameter binding"""
import sys
sys.path.insert(0, 'flask_app')
from db import execute_query

# Try with user_id = 2 (which exists)
query = 'SELECT user_id, username FROM USERS WHERE user_id = %(user_id)s'
result = execute_query(query, {'user_id': 2})
print(f'With parameter (%(user_id)s = 2): {result}')

# Also try with 3
result2 = execute_query(query, {'user_id': 3})
print(f'With user_id=3: {result2}')

# Try without parameter
query3 = 'SELECT user_id, username FROM USERS WHERE user_id = 2'
result3 = execute_query(query3)
print(f'Without parameter (hard-coded 2): {result3}')
