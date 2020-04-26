# Outdated
I stopped developing this version due to it's limitations when using py2app and it being only useful for OSX. The appearance of PySimpleGUI has inspired me to remake this app as a completely standalone app with no need for connecting to a web server at all.

Check the new 2020 version here https://github.com/antonvino/preciousapp

# About
Precious Mac OS X app is the standalone part of the hour logging app that I've called Precious. It comes from a quote of a cool french guy who said to me once "I'm sorry but I work and my time is precious".
It is a side project that I'm working on to learn Python and also to help my discipline.
The hours are logged via this app. It is made with PyObjC wrappers using XCode to create the interface.
There is a web app that outputs the data that is pushed to it via this app. The web app is here: https://github.com/antonvino/precious_web


# How to contribute
Feel free to contribute to the app and do a pull request if you want to work on bugs or implement new features. I'm trying to keep the Mac OS X app minimal, so will not approve any fancy upgrades. Feel free to create your own app based on my code and if it works well we can figure out the syncing to the web side as well.

# py2app commands
Alias build:
python setup.py py2app -A

Launch to test:
dist/Precious.app/Contents/MacOS/Precious

Dist build:
python setup.py py2app

