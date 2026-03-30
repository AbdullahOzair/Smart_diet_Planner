import sys; sys.path.insert(0, './flask_app')
from app import app
with app.app_context():
    from flask import session
    with app.test_request_context('/user/dashboard'):
        session['user_id'] = 1
        session['user_role'] = 'user'
        session['first_name'] = 'Dummy'
        try:
            res = app.dispatch_request()
            html = res if type(res) == str else res.get_data(as_text=True)
            print('HTML Length:', len(html))
            if len(html) < 20000: print('Looks small!')
            else: print('Success!')
        except Exception as e:
            print('EXCEPTION:', type(e), e)
