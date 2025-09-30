from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_dynamic_model(model_name: str):
    """
    Retrieve a model class dynamically based on the model name.
    The model must be listed in the ALLOWED_MODELS setting.
    """
    model_name_lower = model_name.lower()

    for app_label, models in settings.ALLOWED_MODELS.items():
        models_dict = {m.lower(): m for m in models}

        if model_name_lower in models_dict:
            real_model_name = models_dict[model_name_lower]

            try:
                model = apps.get_model(app_label, real_model_name)
                if model is None:
                    raise LookupError(f"Model '{real_model_name}' not found in app '{app_label}'.")
                return model
            except LookupError:
                raise LookupError(f"Model '{real_model_name}' not found in app '{app_label}'.")
            except Exception as e:
                raise ImproperlyConfigured(f"Error retrieving model '{real_model_name}': {str(e)}")
            
    raise LookupError(f"Model '{model_name}' is not allowed.")
