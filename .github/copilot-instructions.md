# AI Coding Agent Instructions - Dynamic API Project

## Project Overview

This is a Django-based REST API that provides a **single universal endpoint** for CRUD operations across multiple databases and models. The core innovation is query parameter-based routing: `/api/v1/?db=db1&table=product` dynamically accesses any model in any database without hardcoded endpoints.

## Architecture & Data Flow

### Multi-Database Design

```
├── default db (db.sqlite3) - Django auth/admin tables + custom User model
├── db1 (db1.sqlite3) - Products & Categories (e-commerce domain)
├── db2 (db2.sqlite3) - Animals, Species & Breeds (veterinary domain)
└── db3 (db3.sqlite3) - Movies & Genres (entertainment domain)
```

### Request Flow Pattern

1. **URL**: `/api/v1/?db=db1&table=product` (query params, not path segments)
2. **Core Logic**: `apps.core.utils.get_model_from_path()` resolves model from params
3. **Database Router**: `config.routers.DatabaseRouter` enforces isolation
4. **Dynamic Serializer**: `DynamicModelSerializer` adapts to any model structure
5. **ViewSet**: Single `DynamicModelViewSet` handles all models

## Critical Implementation Patterns

### Dynamic Model Resolution

```python
# apps/core/utils.py - Core discovery logic
def get_model_from_path(database_name: str, model_name: str):
    # Validates database exists, finds model by name across all apps
    # Verifies table exists in target database before returning
```

### Database Routing Rules (config/routers.py)

- `app1` models → `db1` database
- `app2` models → `db2` database
- `app3` models → `db3` database
- `auth`/`admin`/`core` models → `default` database (enforced)

### UUID Primary Keys Convention

All models use `UUIDField(primary_key=True, default=uuid4)` for consistent identification across databases.

## Development Workflows

### Adding New Database Context

1. Create new app: `python manage.py startapp app4`
2. Add database config to `settings.DATABASES['db4']`
3. Update `routers.DatabaseRouter.route_app_labels['app4'] = 'db4'`
4. Create models with UUID primary keys
5. Run migrations: `python manage.py migrate --database=db4`

### Testing Dynamic API

```bash
# Populate test data across all databases
python scripts/populate_databases.py

# Test endpoints
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8000/api/v1/?db=db1&table=product"
```

### Authentication Flow

```bash
# Get tokens
curl -X POST http://localhost:8000/api/v1/token/ \
  -d '{"username":"admin","password":"admin"}'

# Use access token (5-minute lifetime)
curl -H "Authorization: Bearer <access_token>" <endpoint>
```

## Project-Specific Conventions

### Query Parameter Validation

`DynamicModelViewSet.initial()` enforces required `db` and `table` params on every request.

### Environment Configuration

```python
# Required .env variables
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
# Optional database overrides
DB1_ENGINE=django.db.backends.postgresql
DB1_NAME=custom_db1_name
```

### Custom Auth Model

`AUTH_USER_MODEL = "apps.auth.User"` extends AbstractUser with UUID primary key.

## API Documentation & Testing

- **OpenAPI Schema**: `http://localhost:8000/api/schema/`
- **Swagger UI**: `http://localhost:8000/api/schema/swagger-ui/`
- **ReDoc**: `http://localhost:8000/api/schema/redoc/`

## Integration Points

### CORS Configuration

Preconfigured for `localhost:3000` (frontend) and `localhost:8000` (API) in development.

### JWT Token Settings

- Access token: 5 minutes (short for security)
- Refresh token: 1 day
- Token blacklisting enabled for logout functionality

### Migration Strategy

Always specify database: `python manage.py migrate --database=db1`
Use `scripts/populate_databases.py` for consistent test data across environments.
