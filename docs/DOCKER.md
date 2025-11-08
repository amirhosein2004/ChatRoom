# Docker Guide

Quick guide for Docker deployment.

## Overview

The application has three Docker environments:

- **Development**: Currently active and working
- **Staging**: Coming soon
- **Production**: Coming soon

Each environment has its own configuration and bash scripts that automatically handle setup tasks.

---

## Running the Application

### Development Environment (Active)

```bash
docker-compose -f docker/environments/development/docker-compose.dev.yml up --build
```

Access at: http://localhost:8000

### Staging Environment (Coming Soon)

```bash
docker-compose -f docker/environments/staging/docker-compose.staging.yml up --build
```

### Production Environment (Coming Soon)

```bash
docker-compose -f docker/environments/production/docker-compose.prod.yml up --build
```

---

## Bash Scripts

Each environment uses automated bash scripts for setup:

### Development Script (`entrypoint.dev.sh`)

Automatically performs:
- Wait for database and Redis connection
- Run database migrations
- Collect static files  
- Create admin superuser (username: admin, password: admin123)
- Start development server with hot-reload

### Staging Script (`entrypoint.staging.sh`) - Coming Soon

Will handle staging environment setup.

### Production Script (`entrypoint.sh`) - Coming Soon

Will handle production environment setup.

---

[← Back to Documentation Index](README.md)
