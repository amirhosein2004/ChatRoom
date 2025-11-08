# Django Chat Application

![Chat Application](docs/assets/Screenshot%202025-11-08%20121735.png)

A real-time chat application built with Django, Django Channels, Redis, and PostgreSQL. This application supports multiple chat rooms, real-time messaging, image sharing, and message history with infinite scroll.

## 🚀 Features

- **Real-time Chat**: WebSocket-based real-time messaging using Django Channels
- **Room Management**: Create and manage multiple chat rooms
- **Image Sharing**: Send and receive images in chat
- **Message History**: Scroll up to load previous messages (infinite scroll)
- **User Authentication**: Secure user authentication and authorization
- **Public/Private Rooms**: Support for both public and private chat rooms
- **Responsive UI**: Modern, user-friendly interface with templates
- **RESTful API**: Complete REST API for integration
- **Docker Support**: Fully containerized with Docker for easy deployment

## 📋 Prerequisites

- Docker and Docker Compose
- Git

## 🐳 Docker Environments

This project includes three Docker environments:

### Development (Currently Active)

Run the development environment:

```bash
docker-compose -f docker/environments/development/docker-compose.dev.yml up --build
```

Superuser info:
- **supser user** : admin
- **password** : admin123

Access the application:
- **Application**: http://127.0.0.1:8000/api/room/v1/rooms/list/
- **Public room**: http://127.0.0.1:8000/api/room/v1/chat/
- **Admin Panel**: http://localhost:8000/admin

### Staging (Coming Soon)

Run the staging environment:

```bash
docker-compose -f docker/environments/staging/docker-compose.staging.yml up --build
```

### Production (Coming Soon)

Run the production environment:

```bash
docker-compose -f docker/environments/production/docker-compose.prod.yml up --build
```

## 🏗️ Architecture

The application is built with:

- **Backend**: Django 4.x + Django REST Framework
- **Real-time**: Django Channels + Redis
- **Database**: PostgreSQL
- **WebSockets**: ASGI with Daphne
- **Containerization**: Docker + Docker Compose

## 📚 Documentation

For detailed documentation, please visit the [docs](docs/) directory:

- [Complete Documentation Index](docs/README.md)
- [Models Documentation](docs/MODELS.md)
- [Templates Documentation](docs/TEMPLATES.md)
- [API Documentation](docs/API.md)
- [User Guide](docs/USER_GUIDE.md)
- [Project Structure](docs/PROJECT_STRUCTURE.md)
- [Docker & Technical Guide](docs/DOCKER.md)

## 🚦 Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd ChatPage
```

2. Create environment file:
```bash
cp .env.examples /docker/environments/development/.env.dev
```

3. Update the `.env` file with your configuration

4. Run the development environment:
```bash
docker-compose -f docker/environments/development/docker-compose.dev.yml up --build
```

6. Access the application at http://127.0.0.1:8000/api/room/v1/rooms/list/

## 🛠️ Tech Stack

- **Django**: Web framework
- **Django REST Framework**: API development
- **Django Channels**: WebSocket support
- **Redis**: Channel layer backend
- **PostgreSQL**: Database
- **Docker**: Containerization
- **Nginx**: Reverse proxy (production)

## 📝 License

This project is licensed under the MIT License.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support, please open an issue in the repository.
