from models.tables.sessions import Sessions
from functions.users import require_login

@require_login
def logout(response, user):
    key = response.get_secure_cookie("session_id").decode('utf-8')
    Sessions().delete(key)
    response.redirect('/login')
