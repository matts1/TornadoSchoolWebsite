from . import render
from functions.users import require_login
from models.tables.classes import Classes

@require_login
def classes(response, user):
    if user.is_student():
        year = name = error = success = ""
        key = response.get_field('key')
        if key != None:
            res = Classes().join(user.id, key)
            if res[0]:
                success = res[1]
            else:
                error = res[1]
        classes = user.getStudentClasses()
    else:
        name = response.get_field("name")
        year = response.get_field("year")
        key = response.get_field("key")
        success, error = Classes().add(user.id, name, year, key)
        classes = user.getTeacherClasses()
    render("/users/classes.html", response, {
        "err": error,
        "success": success,
        "year": year if year else 7,
        "name": name if name else "",
        "classes": classes
    })