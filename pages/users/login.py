from . import render
from models.tables.users import Users
from models.tables.sessions import Sessions
from functions.users import require_no_login

@require_no_login
def login(response, user):
    email = response.get_field("email")
    password = response.get_field("pwd")
    result = Users().login(email, password)
    if result == None:
        err = ""
    elif result == False:
        err = "The username or password was incorrect"
    elif result.state in [0, 2]:
        err = result.email + " has not been activated yet. Please look at the email sent to you (it may have been put in spam)"
    elif result.state == 3:
        err = result.email + " has not been validated by an admin yet."
    else:
        sessionid = Sessions().register(result.id)
        response.set_secure_cookie('session_id', sessionid)
        return response.redirect("/home")

    render("users/login.html", response, {"err": err})
