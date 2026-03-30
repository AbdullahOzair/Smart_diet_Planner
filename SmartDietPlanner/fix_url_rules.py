with open('flask_app/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('<int%(user_id)s>', '<int:user_id>')
text = text.replace('<int%(goal_id)s>', '<int:goal_id>')
text = text.replace('<int%(log_id)s>', '<int:log_id>')

with open('flask_app/app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Fixed <int:var>")