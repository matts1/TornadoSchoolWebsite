from tornado import Server

from os import path
import sys
sys.path.append(path.dirname(path.realpath(__file__)))

from pages import *

server = Server()
server.register('/', index)
server.register('/login', login)
server.register('/signup', signup)
server.register('/activate/([a-zA-Z0-9]+)', activate)

server.run()

