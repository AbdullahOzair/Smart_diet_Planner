with open('flask_app/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

missing_views = ['admin_activities', 'admin_delete_user', 'change_password', 'verify_reset_code', 'admin_meal_logs', 'admin_daily_logs', 'admin_view_user', 'admin_update_user', 'admin_goals', 'admin_meals', 'admin_add_activity', 'admin_users', 'admin_mood_logs', 'admin_create_user', 'admin_activity_logs', 'forgot_password', 'admin_suggestions', 'admin_reports', 'reset_password', 'admin_add_meal']

# prepare dummy routes
routes_code = "\n# --- Dummy routes for missing endpoints ---\n"
for v in missing_views:
    if v in ('admin_delete_user', 'admin_view_user', 'admin_update_user'):
        routes_code += f"""
@app.route('/{v}/<int:id>', methods=['GET', 'POST'])
def {v}(id): return "Dummy {v}"
"""
    else:
        routes_code += f"""
@app.route('/{v}', methods=['GET', 'POST'])
def {v}(): return "Dummy {v}"
"""

# insert before if __name__ == '__main__':
parts = text.split("if __name__ == '__main__':")
if len(parts) > 1:
    new_text = parts[0] + routes_code + "\nif __name__ == '__main__':" + parts[1]
    with open('flask_app/app.py', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('Dummy routes injected successfully!')
else:
    print('Could not find if __name__ block')
