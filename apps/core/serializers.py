from uuid import UUID

from django.db import models
from rest_framework import serializers

from apps.core.utils import get_database_for_model


class DynamicModelSerializer(serializers.ModelSerializer):
    """
    A dynamic ModelSerializer that can adapt to any model.
    """

    class Meta:
        model = None
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """
        Initialize serializer with dynamic model.

        The model must be passed as a kwarg 'model' when instantiating the serializer.
        """
        self.database = kwargs.pop("database", None)
        self.Meta.model = kwargs.pop("model", None)
        if not self.Meta.model:
            raise ValueError("You must pass a model to DynamicModelSerializer")
        if not self.database:
            self.database = get_database_for_model(self.Meta.model, None)
        super().__init__(*args, **kwargs)

        # Configure fields for UUID primary keys and foreign keys
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.PrimaryKeyRelatedField):
                # Set the correct database for foreign key querysets
                field.queryset = field.queryset.using(self.database)

    def to_internal_value(self, data):
        """
        Override to_internal_value to handle database-specific lookups.
        """
        # The serializer fields are already configured in __init__ to use the correct database
        return super().to_internal_value(data)

    def create(self, validated_data):
        """
        Create a new instance of the model using the specified database.
        """
        return self.Meta.model.objects.using(self.database).create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update an existing instance of the model using the specified database.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save(using=self.database)
        return instance