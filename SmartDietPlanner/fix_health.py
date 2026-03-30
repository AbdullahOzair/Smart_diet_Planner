with open('flask_app/app.py', 'r', encoding='utf-8') as f:
    content = f.read()
import re
content = content.replace(
    "render_template('user_dashboard.html', stats=stats, today_tracking=today_tracking, user_profile=user_prof[0] if user_prof else [])",
    "render_template('user_dashboard.html', stats=stats, today_tracking=today_tracking, user_profile=user_prof[0] if user_prof else [], health_metrics={})"
)
with open('flask_app/app.py', 'w', encoding='utf-8') as f:
    f.write(content)
