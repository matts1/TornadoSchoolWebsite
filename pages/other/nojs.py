from template_engine.main import Parser
import re

def nojs(response):
    page = render("nojs.html", None)
    response.write(re.sub("<noscript>.*?</noscript>", "", page))
