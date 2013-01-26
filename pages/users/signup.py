from . import render
from models.tables.users import Users
from functions.users import require_no_login
students = Users()

@require_no_login
def signup(response, user):
    fields = ["email", "first", "last", "pwd", "conf-pwd", "teacher"]
    fields = [response.get_field(field) for field in fields]
    success = students.register(fields)
    render("users/register.html", response, {"success": success, "email": fields[0]})
