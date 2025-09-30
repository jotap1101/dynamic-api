from django.conf import settings

class DatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label in settings.ALLOWED_MODELS:
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in settings.ALLOWED_MODELS:
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (obj1._meta.app_label in settings.ALLOWED_MODELS and
                obj2._meta.app_label in settings.ALLOWED_MODELS):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in settings.ALLOWED_MODELS:
            return db in settings.ALLOWED_DATABASES
        return None