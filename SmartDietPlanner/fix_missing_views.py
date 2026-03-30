with open('flask_app/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("render_template('user_dashboard.html', view='user_add_water')", "render_template('user_dashboard.html', view='add_water')")
text = text.replace("render_template('user_dashboard.html', view='user_progress')", "render_template('user_dashboard.html', view='progress', health_metrics={})")

with open('flask_app/app.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Views fixed!")
