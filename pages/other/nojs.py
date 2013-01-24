from template_engine.main import Parser
import re

def nojs(response):
    page = Parser("nojs.html").parse().eval({"title": "Please Enable Javascript"})
    response.write(re.sub("<noscript>.*?</noscript>", "", page))
