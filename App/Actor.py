from functools import wraps
from flask import g, request, redirect, session

class Actor:
    def __init__(self, sess_key="", route_url="/"):
        self.sess_key = sess_key
        self.route_url = route_url

    def uid(self):
        return session.get(self.sess_key, "err") if self.isLoggedIn() else "err"

    def set_session(self, session, g):
        g.user = session.get(self.sess_key, 0) if self.isLoggedIn() else 0

    def isLoggedIn(self):
        return session.get(self.sess_key, 0) > 0

    def login_required(self, f, path="signin"):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get(self.sess_key):
                print(path)
                return redirect(self.route_url + path)
            return f(*args, **kwargs)
        return decorated_function

    def redirect_if_login(self, f, path="/"):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get(self.sess_key):
                return redirect(self.route_url + path)
            return f(*args, **kwargs)
        return decorated_function

    def signout(self):
        session[self.sess_key] = None

    def signin(self):
        pass
