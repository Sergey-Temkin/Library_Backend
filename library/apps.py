# library/apps.py
from django.apps import AppConfig


# Defines app settings for Django
class LibraryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "library"
