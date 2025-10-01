# AI Coding Agent Instructions - Dynamic API Project

## Project Overview

This is a Django-based REST API project with a modular structure organized into apps. The project uses Django REST Framework (DRF) for API development and follows a structured approach to building dynamic APIs.

## Project Structure

- `config/` - Core Django project configuration
- `apps/` - Main application modules
  - `core/` - Central application module
  - Additional modular apps (`app1`, `app2`, `app3`)

## Key Technologies & Dependencies

- Django 5.2.6 with REST Framework 3.16.1
- JWT Authentication (djangorestframework_simplejwt)
- API Documentation (drf-spectacular)
- Redis for caching
- Environment management with django-environ

## Development Environment Setup

1. Environment Variables:

   - Project uses `.env` file for configuration
   - Required variables: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
   - See `config/settings.py` for environment variable usage

2. Development Workflow:

   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # Linux/Mac

   # Install dependencies
   pip install -r requirements.txt

   # Run migrations
   python manage.py migrate

   # Start development server
   python manage.py runserver
   ```

## Project Conventions

1. App Organization:

   - Each app follows standard Django structure with models, views, urls
   - Core functionality in `apps.core`
   - Additional apps modularized for specific features

2. API Development:
   - Uses DRF for API endpoints
   - API documentation with drf-spectacular
   - JWT for authentication

## Common Development Tasks

- Create new app: `python manage.py startapp app_name`
- Generate migrations: `python manage.py makemigrations`
- Run tests: `python manage.py test`
- Create superuser: `python manage.py createsuperuser`

## Key Integration Points

1. URL Configuration:

   - Main URLs defined in `config/urls.py`
   - App-specific URLs in respective `app_name/urls.py`

2. Authentication:

   - JWT-based authentication system
   - Token configuration in settings

3. Caching:
   - Redis integration for caching
   - Cache settings in Django configuration

## Best Practices

1. Always use environment variables for sensitive data
2. Follow Django's app-based modular structure
3. Implement proper API versioning
4. Use Django's built-in testing framework
