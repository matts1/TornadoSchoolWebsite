from . import render
from functions.users import get_level
from models.tables.users import Users
users = Users()

@get_level
def reset(response, reset_key, user):
    if user == None:
        user = users.get_users_by_reset(reset_key)
    if user != None: #user is logged in or has valid key
        pwd = response.get_field("pwd")
        conf_pwd = response.get_field("conf_pwd")
        success = ""
        if conf_pwd == pwd and pwd not in ["", None] and len(pwd) >= 6:
            user.chgPwd(pwd)
            success = "Your password has been reset"
        context = {"displayreset": True, "success": success}
    else:#not logged in and not valid reset key
        email = response.get_field("email")
        err = success = ""
        if email != None and not email.isdigit():
            try:
                user = users.get_activated_user(email)
                user.prepareReset()
                success = "An email has been sent to {} giving information on how to reset your password".format(email)
            except ValueError as e:
                err = str(e)

        context = {"displayreset": False, "err": err, "success": success}
    render("users/reset.html", response, context)