from models.tables.users import Users
from functions.users import get_level
users = Users()

@get_level
def activate(response, key):
    users.activate(key)
    response.redirect("/login")
