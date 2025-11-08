# Project Structure

Quick overview of the Django Chat Application structure.

## Directory Structure

```
ChatPage/
├── app_room/                    # Main chat application
│   ├── api/                     # API layer
│   │   ├── v1/                  # API version 1
│   │   │   ├── consumers/       # WebSocket consumers
│   │   │   │   ├── __init__.py
│   │   │   │   └── chat_consumers.py
│   │   │   ├── routing/         # WebSocket routing
│   │   │   │   ├── __init__.py
│   │   │   │   └── websocket.py
│   │   │   ├── serializers/     # DRF serializers
│   │   │   │   ├── __init__.py
│   │   │   │   └── message_serializers.py
│   │   │   ├── urls/            # URL configurations
│   │   │   │   ├── __init__.py
│   │   │   │   ├── messages.py
│   │   │   │   ├── room.py
│   │   │   │   └── room_management.py
│   │   │   ├── views/           # API views
│   │   │   │   ├── __init__.py
│   │   │   │   ├── message_views.py
│   │   │   │   ├── room_management_views.py
│   │   │   │   └── room_views.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── migrations/              # Database migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_remove_message_room_delete_room.py
│   │   ├── 0003_room_message_room.py
│   │   └── ...
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   └── room.py
│   ├── __init__.py
│   ├── admin.py                 # Django admin configuration
│   ├── apps.py                  # App configuration
│   ├── routing.py               # WebSocket routing
│   ├── tests.py                 # Unit tests
│   └── urls.py                  # URL patterns
│
├── chat/                        # Django project settings
│   ├── settings/                # Split settings
│   │   ├── __init__.py
│   │   ├── base.py              # Base settings
│   │   ├── development.py       # Development settings
│   │   ├── staging.py           # Staging settings
│   │   └── production.py        # Production settings
│   ├── __init__.py
│   ├── asgi.py                  # ASGI configuration
│   ├── routing.py               # Main WebSocket routing
│   ├── urls.py                  # Main URL configuration
│   └── wsgi.py                  # WSGI configuration
│
├── configs/                     # Configuration files
│   ├── init-db.sql              # Database initialization
│   └── redis.conf               # Redis configuration
│
├── docker/                      # Docker configurations
│   ├── environments/            # Environment-specific configs
│   │   ├── development/         # Development environment
│   │   │   ├── docker-compose.dev.yml
│   │   │   └── .env.dev
│   │   ├── staging/             # Staging environment
│   │   │   ├── docker-compose.staging.yml
│   │   │   └── .env.staging
│   │   └── production/          # Production environment
│   │       ├── docker-compose.prod.yml
│   │       └── .env.prod
│   ├── scripts/                 # Deployment scripts
│   │   ├── entrypoint.dev.sh    # Development entrypoint
│   │   ├── entrypoint.staging.sh
│   │   └── entrypoint.sh        # Production entrypoint
│   └── .dockerignore            # Docker ignore patterns
│
├── docs/                        # Documentation
│   ├── assets/                  # Images and screenshots
│   │   ├── Screenshot 2025-11-08 121735.png
│   │   └── Screenshot 2025-11-08 121940.png
│   ├── API.md                   # API documentation
│   ├── DOCKER.md                # Docker guide
│   ├── MODELS.md                # Models documentation
│   ├── PROJECT_STRUCTURE.md     # This file
│   ├── README.md                # Documentation index
│   ├── TEMPLATES.md             # Templates documentation
│   └── USER_GUIDE.md            # User guide
│
├── requirements/                # Python dependencies
│   ├── base.txt                 # Base requirements
│   ├── development.txt          # Development requirements
│   ├── staging.txt              # Staging requirements
│   └── production.txt           # Production requirements
│
├── staticfiles/                 # Collected static files
│   ├── admin/                   # Django admin static files
│   ├── debug_toolbar/           # Debug toolbar assets
│   └── rest_framework/          # DRF static files
│
├── templates/                   # HTML templates
│   └── chat/                    # Chat templates
│       ├── create_room.html     # Room creation form
│       ├── room.html            # Chat room interface
│       └── room_list.html       # Room list page
│
├── .env.examples                # Environment variables example
├── .gitignore                   # Git ignore patterns
├── manage.py                    # Django management script
└── README.md                    # Project README
```

---

## Key Components

- **app_room/**: Main application with models, views, and API
- **chat/**: Django settings and configuration
- **docker/**: Docker configurations for 3 environments
- **templates/**: HTML templates for chat interface
- **docs/**: Documentation files

---

## Features

- ✓ Real-time messaging via WebSocket
- ✓ Create and join chat rooms
- ✓ Send text and image messages
- ✓ Message history with infinite scroll
- ✓ Guest user system

---

## Technology Stack

- **Backend**: Django + Django Channels
- **Database**: PostgreSQL
- **Cache**: Redis
- **Frontend**: Vanilla JavaScript
- **Deployment**: Docker

---

[← Back to Documentation Index](README.md)
