
import sys; sys.path.insert(0, './flask_app')
from app import app
with app.app_context():
    from flask import session
    with app.test_request_context('/api/add-water-glass', method='POST'):
        session['user_id'] = 1
        try:
            res = app.dispatch_request()
            print('STATUS:', res.status_code)
            print('DATA:', res.get_data(as_text=True))
        except Exception as e:
            print('EXCEPTION:', type(e), e)

