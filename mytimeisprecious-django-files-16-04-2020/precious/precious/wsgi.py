"""
WSGI config for precious project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import sys
print '=== PYTHON VERSION ==='
print (sys.version) #parentheses necessary in python 3.

import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('~/.virtualenvs/precious_web/lib/python2.7/site-packages')

# add the virtualenv site-packages path to the sys.path
sys.path.append('~/.virtualenvs/precious_web/lib/python2.7/site-packages')
# add the hellodjango project path into the sys.path
sys.path.append('/srv/www/mytimeisprecious.com/precious_web')
sys.path.append('/srv/www/mytimeisprecious.com/precious_web/precious')
sys.path.append('/var/lib/gems/1.8/gems/sass-3.4.18/bin/sass')
import os

# os.environ.setdefault("PYTHONPATH", "~/.virtualenvs/precious_web/lib/python2.7/site-packages")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "precious.settings.production")

application = get_wsgi_application()
