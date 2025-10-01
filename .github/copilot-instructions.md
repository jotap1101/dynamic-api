# AI Coding Agent Instructions - Dynamic API Project

## Project Overview

This is a Django-based REST API project that enables dynamic database and model access through URL patterns. The project uses Django REST Framework (DRF) and follows a multi-database architecture where different apps use separate databases. The core API is built to dynamically route requests to appropriate databases and models based on URL parameters.

## Project Structure

- `config/` - Core Django project configuration
- `apps/` - Main application modules
  - `core/` - Central API module with dynamic routing
  - `app1/` - First context module using database 'db1'
  - `app2/` - Second context module using database 'db2'
  - `app3/` - Third context module using database 'db3'

### Database Architecture

- Each app (except core) has its own dedicated database
- Default database contains Django's built-in tables (auth, admin, etc.)
- Database routing is handled through URL patterns: `/api/v1/<database_name_or_alias>/<model_name_or_alias>/`

## Key Technologies & Dependencies

- Django 5.2.6 with REST Framework 3.16.1
- JWT Authentication (djangorestframework_simplejwt)
- API Documentation (drf-spectacular)
- Redis for caching
- Environment management with django-environ
- CORS handling with django-cors-headers

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
   - Core functionality in `apps.core` handles API routing and authentication
   - Context apps (`app1`, `app2`, `app3`) contain models and business logic

2. API Development:
   - Uses DRF ModelViewSets and ModelSerializers for CRUD operations
   - Dynamic routing based on database and model aliases
   - Custom actions with `@action` decorator for non-CRUD operations
   - RESTful conventions for endpoint design
   - Protected access using JWT authentication
   - CORS configuration for controlled cross-origin access

## Common Development Tasks

- Create new app: `python manage.py startapp app_name`
- Generate migrations: `python manage.py makemigrations`
- Run tests: `python manage.py test`
- Create superuser: `python manage.py createsuperuser`

## Key Integration Points

1. URL Configuration:

   - Main URLs defined in `config/urls.py`
   - App-specific URLs in respective `app_name/urls.py`

2. Authentication & Security:

   - JWT-based authentication using djangorestframework_simplejwt
   - Token configuration in settings
   - CORS configuration via django-cors-headers
   - Custom permissions to secure database/model access

3. Caching:
   - Redis integration for caching
   - Cache settings in Django configuration

## Best Practices

1. Always use environment variables for sensitive data
2. Follow Django's app-based modular structure
3. Implement proper API versioning
4. Use Django's built-in testing framework
5. Follow RESTful conventions for endpoint design
6. Secure database and model access through proper authentication and permissions
7. Use custom actions (@action decorator) for non-CRUD operations within ViewSets
8. Keep database context isolated within respective apps
