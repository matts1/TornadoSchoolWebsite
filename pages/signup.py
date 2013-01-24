from . import render
from models.tables.users import Users
students = Users()

def signup(response):
    fields = ["email", "first", "last", "pwd", "conf-pwd"]
    fields = [response.get_field(field) for field in fields]
    success = students.register(fields)
    render("users/register.html", response, {"success": success, "email": fields[0]})
