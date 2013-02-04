from functions.users import require_admin
from models.tables.users import Users
from models.tables.sessions import Sessions
from models.rows.users import User
from . import render

@require_admin
def users(response, user):
    teachers = Users().get_teachers()
    for teacher in teachers:
        newstate = response.get_field("level{}".format(teacher.id))
        if newstate != None and newstate.isdigit() and 2 < int(newstate) < 6:
            if int(newstate) < teacher.state:
                Sessions().deleteuser(teacher.id)
            teacher.state = int(newstate)
            teacher.save()
    user.discard()
    if user.state != 5:
        response.redirect("/login")
    render("users/manage.html", response, {"teachers": teachers})