import sys
sys.path.insert(0, 'flask_app')
from db import execute_query
for i,r in enumerate(res): print(f'{i}: {r[0]}')
