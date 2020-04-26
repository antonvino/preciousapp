# About
Precious web app is the web side of the hour logging app that I've called Precious. It comes from a quote of a cool french guy who said to me once "I'm sorry but I work and my time is precious".
It is a side project that I'm working on to learn Django and also to help my discipline.
The hours are logged via a MacOSX app that I made using PyObjC and that can be found here: https://github.com/antonvino/precious_mac


# How to contribute
Feel free to contribute to the app and do a pull request if you want to work on bugs or implement new features.

## Setup
# 1. Creating virtualenv

Create a new env:
> mkvirtualenv precious_web
> workon precious_web
> pip install -r requirements.txt

# 2. Reset db command
First create the database
CREATE DATABASE precious_db;

# 3. Run server
Launch your virtual environment for the project:
> workon precious_web

Locate your project's manage.py (using cd) and do:
> python manage.py runserver

If it doesn't work and if there is no folder "static" in the project root, create it

# How to run the tests
python manage.py test logs.tests