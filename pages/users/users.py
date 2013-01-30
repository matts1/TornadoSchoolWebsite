from functions.users import require_admin
from models.tables.users import Users
from . import render

@require_admin
def users(response, user):
    teachers = Users().get_teachers()
    render("users/manage.html", response, {"teachers": teachers})