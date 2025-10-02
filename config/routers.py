class DatabaseRouter:
    """
    A router to control database operations for multiple databases.
    Maps each app to its specific database:
    - app1 -> db1
    - app2 -> db2
    - app3 -> db3
    - All others -> default (db.sqlite3)
    """

    route_app_labels = {
        "app1": "db1",
        "app2": "db2",
        "app3": "db3",
    }

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to default db.
        """
        if model._meta.app_label in self.route_app_labels:
            return self.route_app_labels[model._meta.app_label]
        return "default"

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to default db.
        """
        if model._meta.app_label in self.route_app_labels:
            return self.route_app_labels[model._meta.app_label]
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both objects are in the same database
        or if one of them is in the default database.
        """
        db1 = self.route_app_labels.get(obj1._meta.app_label)
        db2 = self.route_app_labels.get(obj2._meta.app_label)

        # Allow if both models are in the same database
        if db1 and db2 and db1 == db2:
            return True
        # Allow if either model is in default database
        if not db1 or not db2:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that the auth and contenttypes apps only appear in the
        default database, and apps with specific databases only appear
        in their respective databases.
        """
        # If the app has a specific database assigned
        if app_label in self.route_app_labels:
            return db == self.route_app_labels[app_label]
        # All other apps go to the default database
        return db == "default"
