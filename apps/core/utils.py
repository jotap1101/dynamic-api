from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def get_dynamic_model(model_name: str):
    """
    Retrieve a model class dynamically based on the model name.
    The model must be listed in the ALLOWED_MODELS setting.
    """
    model_path = settings.ALLOWED_MODELS.get(model_name)

    if not model_path:
        raise LookupError(f"Model '{model_name}' is not allowed.")
    
    try:
        app_label, model_name = model_path.split('.')
        return apps.get_model(app_label, model_name)
    except (ValueError, LookupError) as e:
        raise ImproperlyConfigured(f"Error retrieving model '{model_path}': {e}")

