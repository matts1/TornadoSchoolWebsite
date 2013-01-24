from models.tables.users import Users
users = Users()

def activate(response, key):
    users.activate(key)
    response.redirect("/login")
