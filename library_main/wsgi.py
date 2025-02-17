# library_main/wsgi.py

# !/usr/bin/env python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_main.settings")

application = get_wsgi_application()
