"""
Settings package for ChatPage project.
Automatically imports the appropriate settings module based on the DJANGO_SETTINGS_MODULE environment variable.
"""
import os

# Get the environment from DJANGO_SETTINGS_MODULE or default to development
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'chat.settings.development')

if 'production' in settings_module:
    from .production import *
elif 'development' in settings_module:
    from .development import *
else:
    # Default to development settings
    from .development import *
