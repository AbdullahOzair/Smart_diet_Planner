import sys
sys.path.insert(0, './flask_app')
from app import app
client = app.test_client()
with client.session_transaction() as sess:
    sess['user_id'] = 1
    sess['role'] = 'user'
res = client.get('/user/dashboard')
text = res.data.decode('utf-8')
print('Status:', res.status_code)
import re
print('BMI Matches:', [m for m in text.split('\n') if 'BMI' in m.upper()])
