from . import render

def login(response):
    render("users/login.html", response)
