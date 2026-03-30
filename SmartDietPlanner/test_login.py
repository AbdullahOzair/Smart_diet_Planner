
import requests

s = requests.Session()
# Attempt a login or fake one. Actually, lets just render the template manually using flask app context
from flask_app.app import app
with app.app_context():
    from flask import session, render_template
    with app.test_request_context("/user/dashboard"):
        session["user_id"] = 1
        session["user_role"] = "user"
        session["first_name"] = "Dummy"
        from flask_app.app import user_dashboard
        try:
            res = app.dispatch_request()
            print("Status Code:", type(res))
            if hasattr(res, "status_code"):
                print("Code:", res.status_code)
            
            html = res if type(res) == str else res.get_data(as_text=True)
            print("HTML Length:", len(html))
            print("Last 200 chars:")
            print(html[-200:])
        except Exception as e:
            print("EXCEPTION:", repr(e))

