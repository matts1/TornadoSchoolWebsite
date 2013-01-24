from models.tables.users import Users
students = Users()

def activate(response, key):
    students.activate(key)
    response.redirect("/login")
