from tornado import Server
from template_engine.main import Parser

def index(response):
    response.write(Parser('register.html').parse().eval({}))

server = Server()
server.register('/', index)
server.register('/test/blah', index)

server.run()

