"""
Django settings for ChatPage project.

This file imports settings from the modular settings package.
The appropriate settings module is automatically selected based on the environment.

For development: Use chat.settings.development
For production: Use chat.settings.production

You can also set the DJANGO_SETTINGS_MODULE environment variable to specify
which settings module to use.

Example:
    export DJANGO_SETTINGS_MODULE=chat.settings.production
    python manage.py runserver
"""

from .settings import *
