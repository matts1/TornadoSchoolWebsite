from . import render
from functions.users import get_level
from models.tables.users import Users
users = Users()

@get_level
def reset(response, reset_key, user=None):
    print(user)
    user = users.get_users_by_reset(reset_key)
    if False:
        pass#user is logged in
        #replace user variable with variable of logged in user
    elif user == None:#not logged in and not valid reset key
        email = response.get_field("email")
        err = ""
        if email != None and not email.isdigit():
            try:
                user = users.get_activated_user(email)
                user.prepareReset()
            except ValueError as e:
                err = str(e)

        context = {"displayreset": False, "err": err}
        render("users/reset.html", response, context)
        return
    print(user)
    #TODO: before getting this to work, add login capabilities
    context = {"displayreset": True}