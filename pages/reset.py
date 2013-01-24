from . import render
from models.tables.users import Users
students = Users()

def reset(response):
    if False: #if logged in or valid reset key
        pass
    else:
        context = {"displayreset": False}
    render("users/reset.html", response, context)
