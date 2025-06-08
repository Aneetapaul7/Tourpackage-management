# userss/apps.py
from django.apps import AppConfig

class UserssConfig(AppConfig):  # This must match what's in INSTALLED_APPS
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userss'