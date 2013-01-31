from functions.users import require_admin
from models.tables.users import Users
from . import render

@require_admin
def users(response, user):
    teachers = Users().get_teachers()
    for teacher in teachers:
        newstate = response.get_field("level{}".format(teacher.id))
        if newstate != None and newstate.isdigit() and 2 < int(newstate) < 6:
            teacher.state = int(newstate)
            teacher.save()
    render("users/manage.html", response, {"teachers": teachers})