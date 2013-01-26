#decorators defined here
from models.tables.sessions import Sessions
from models.rows.users import User
session = Sessions()

def require_login(fn):
    return auth_level(fn, [1, 4, 5], "/login")

def require_student(fn):
    return auth_level(fn, [4, 5], "/home")

def require_teacher(fn):
    return auth_level(fn, [4, 5], "/home")

def require_admin(fn):
    return auth_level(fn, [5], "/home")

def require_no_login(fn):
    return auth_level(fn, [None], "/home")

def get_level(fn):
    return auth_level(fn, [None, 1, 4, 5], "err")

def get_user(response):
    session_cookie = response.get_secure_cookie("session_id")
    if session_cookie != None:
        session_cookie = session_cookie.decode('utf-8')
        user = session.validate(session_cookie)
        if user != None:
            session.refresh(session_cookie)
            return User(user)
        else:
            return None
    else:
        return None

def auth_level(fn, required_levels, redirect):
    def wrapper(response, *args):
        user = get_user(response)
        if user in required_levels or user.state in required_levels:
            return fn(response, *args, user=user)
        else:
            response.redirect(redirect)
        return None
    return wrapper
