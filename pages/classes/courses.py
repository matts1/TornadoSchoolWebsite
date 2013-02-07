from . import render
from functions.users import require_teacher, require_login

@require_login
def courses_list(response, user):
    response.redirect('/createcourse')

@require_teacher
def create_course(response, user):
    pass

@require_login
def view_course(response, courseid, user):
    pass