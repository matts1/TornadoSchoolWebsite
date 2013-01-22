from . import render

def signup(response):
    render("users/register.html", response)
