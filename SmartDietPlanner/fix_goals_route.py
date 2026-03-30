with open('flask_app/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('def user_goals():\n    \"\"\"User view own goals\"\"\"', '@app.route(\'/user/goals\')\ndef user_goals():\n    \"\"\"User view own goals\"\"\"')

with open('flask_app/app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Fixed user_goals")
