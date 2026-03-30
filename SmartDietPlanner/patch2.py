import codecs

def patchapp():
    with open('flask_app/app.py', 'r', encoding='utf-8') as f:
        text = f.read()

    old_water = '''@app.route('/user/add-water')
def user_add_water():
    """Stub for adding water"""
    return redirect(url_for('user_add_daily_log'))'''

    new_water = '''@app.route('/user/add-water')
def user_add_water():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('user_dashboard.html', view='add_water')'''

    old_prog = '''@app.route('/user/progress')
def user_progress():
    """Stub for user progress"""
    return redirect(url_for('user_profile'))'''

    new_prog = '''@app.route('/user/progress')
def user_progress():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('user_dashboard.html', view='progress', health_metrics=get_user_health_metrics(session['user_id']))'''

    text = text.replace(old_water, new_water)
    text = text.replace(old_prog, new_prog)

    with open('flask_app/app.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Patched.")

patchapp()