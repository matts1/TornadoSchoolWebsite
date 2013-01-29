from . import render
from functions.users import require_login
from models.tables.classes import Classes

@require_login
def classes(response, user):
    if user.state == 1:
        print("student")
    else:
        name = response.get_field("name")
        year = response.get_field("year")
        key = response.get_field("key")
        success, error = Classes().add(user.id, name, year, key)
        render("/users/classes.html", response, {"err": error, "success": success, "year": year if year else 7, "name": name if name else ""})