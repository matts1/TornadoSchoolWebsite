from tornado import Server

from os import path
import sys
sys.path.append(path.dirname(path.realpath(__file__)))

from pages import *

server = Server()
server.register('/', index.index)
server.register('/login', login.login)
server.register('/signup', signup.signup)
server.register('/activate/([a-zA-Z0-9]+)', activate.activate)
server.register('/settings()', settings.settings)
server.register('/settings/([a-zA-Z0-9]+)', settings.settings)
#server.register('/nojs', nojs.nojs)
server.register('/logout', logout.logout)
server.register('/home', home.home)
server.register('/classes', classes.classes)
server.register('/users', users.users)
server.register('/courses', courses.courses_list)
server.register('/createcourse', courses.create_course)
server.register(r'/courses/(\d+)', courses.view_course)

#this needs to go last, since it's a 404 page
server.register('(.*)', missing.missing)

server.run()

