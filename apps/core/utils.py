from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_dynamic_model(table_name: str):
    """
    Retorna a classe Model correspondente ao alias definido em ALLOWED_MODELS.
    """
    model_path = settings.ALLOWED_MODELS.get(table_name)
    if not model_path:
        raise LookupError(f"Tabela '{table_name}' não está autorizada.")

    try:
        app_label, model_name = model_path.split(".")
        return apps.get_model(app_label, model_name)
    except Exception:
        raise ImproperlyConfigured(f"Erro ao carregar model para '{table_name}'.")
