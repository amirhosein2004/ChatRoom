"""
Development settings for ChatPage project.
"""
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Database (PostgreSQL for development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Development-specific apps
INSTALLED_APPS += [
    'debug_toolbar',
]

# Development-specific middleware
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Email backend for development (console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Cache configuration (Redis recommended for development)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
    }
}

# Channels configuration
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],
        },
    },
}

# Logging configuration for development
LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': LEVEL,
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': LEVEL,
            'propagate': False,
        },
    },
}

# Debug toolbar configuration (if used)
INTERNAL_IPS = [
    '127.0.0.1',
]
