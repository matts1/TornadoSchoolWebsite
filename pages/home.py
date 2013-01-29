from functions.users import require_login

@require_login
def home(response, user):
    response.redirect('/classes')