from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import connections
from rest_framework.exceptions import NotFound


def get_model_from_path(database_name: str, model_name: str):
    """
    Retrieves model class based on database and model names from URL.

    Args:
        database_name (str): Name or alias of the database
        model_name (str): Name of the model to retrieve

    Returns:
        Model: Django model class

    Raises:
        NotFound: If database or model is not found
        ValidationError: If validation fails
    """
    # Validate database exists and is accessible
    if database_name not in connections.databases:
        raise NotFound(
            f"Database '{database_name}' is not configured. "
            f"Available databases are: {', '.join(connections.databases.keys())}"
        )

    # Try to establish a connection to verify database is accessible
    try:
        with connections[database_name].cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception as e:
        raise NotFound(
            f"Cannot connect to database '{database_name}'. "
            f"The database might not be running or might have connection issues. "
            f"Error: {str(e)}"
        )

    # Get all apps that might contain our model
    all_models = apps.get_models()
    target_model = None

    # Search for the model in all registered apps
    for model in all_models:
        if model._meta.model_name.lower() == model_name.lower():
            target_model = model
            break

    if not target_model:
        raise NotFound(f"Model '{model_name}' not found")

    # Verify if the table exists in the specified database
    with connections[database_name].cursor() as cursor:
        table_name = target_model._meta.db_table
        try:
            # Try to do a zero-impact query to check if table exists
            cursor.execute(f"SELECT 1 FROM {table_name} WHERE 1=0")
        except Exception:
            raise NotFound(
                f"Table '{table_name}' does not exist in database '{database_name}'. "
                f"Make sure that the model '{model_name}' belongs to the correct database "
                f"and all migrations have been applied."
            )

    return target_model


def get_database_for_model(model, database_name: str):
    """
    Ensures model belongs to the specified database.

    Args:
        model: Django model class
        database_name (str): Name of the database to check

    Returns:
        str: Validated database name

    Raises:
        ValidationError: If database validation fails
    """
    if database_name not in connections.databases:
        available_dbs = ", ".join(connections.databases.keys())
        raise ValidationError(
            f"Database '{database_name}' is not configured. "
            f"Available databases are: {available_dbs}"
        )

    # If model is auth-related, always use default database
    auth_apps = ["auth", "admin", "sessions", "contenttypes"]
    if model._meta.app_label in auth_apps:
        if database_name != "default":
            raise ValidationError(
                f"Model '{model._meta.model_name}' from app '{model._meta.app_label}' "
                f"can only be accessed through the 'default' database, not '{database_name}'. "
                f"Authentication-related models ({', '.join(auth_apps)}) are restricted "
                f"to the default database."
            )
        return "default"

    # Try to establish a connection to verify database is accessible
    try:
        with connections[database_name].cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception as e:
        raise ValidationError(
            f"Cannot connect to database '{database_name}'. "
            f"The database might not be running or might have connection issues. "
            f"Error: {str(e)}"
        )

    return database_name
