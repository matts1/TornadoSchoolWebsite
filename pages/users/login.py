from . import render
from models.tables.users import Users
from models.tables.sessions import Sessions

def login(response):
    email = response.get_field("email")
    password = response.get_field("pwd")
    result = Users().login(email, password)
    print(result)
    if result == None:
        err = ""
    elif result == False:
        err = "The username or password was incorrect"
    elif result.state in [0, 2]:
        err = result.email + " has not been activated yet. Please look at the email sent to you (it may have been put in spam)"
    elif result.state == 3:
        err = result.email + " has not been validated by an admin yet."
    else:
        Sessions().register(result.id)
        return response.redirect("/main")

    render("users/login.html", response, {"err": err})
