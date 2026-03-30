with open('app.py', encoding='utf-8') as f:
    text = f.read()
import re
pos = text.find('@app.')
if pos != -1:
    insert_code = '''
@app.context_processor
def inject_user_profile():
    if 'user_id' in session:
        try:
            profile = execute_query("SELECT * FROM USERS WHERE user_id = :u", {'u': session['user_id']})
            profile = profile[0] if profile else None
            return dict(profile=profile, user_profile=profile)
        except Exception:
            return dict(profile=None, user_profile=None)
    return dict(profile=None, user_profile=None)

'''
    new_text = text[:pos] + insert_code + text[pos:]
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('Injected!')
