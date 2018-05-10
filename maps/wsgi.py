"""
WSGI config for maps project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maps.settings")

# application = get_wsgi_application()


import os
import sys

path = '/home/mohan0925/pythonpoc'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'pythonpoc.settings'
#
## then:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
