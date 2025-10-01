from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import DynamicModelSerializer
from .utils import get_database_for_model, get_model_from_path


class DynamicModelViewSet(viewsets.ModelViewSet):
    """
    A dynamic ViewSet that can handle any model based on URL parameters.
    Provides CRUD operations for any model in any configured database.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = DynamicModelSerializer

    def get_queryset(self):
        """
        Get the list of items for this view.
        Determines the appropriate database and model from the URL.
        """
        database_name = self.kwargs.get("database")
        model_name = self.kwargs.get("model")

        # Get model class based on URL parameters
        model = get_model_from_path(database_name, model_name)

        # Validate and get correct database
        db = get_database_for_model(model, database_name)

        # Return queryset using the appropriate database
        return model.objects.using(db).all()

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs["model"] = get_model_from_path(
            self.kwargs.get("database"), self.kwargs.get("model")
        )
        return serializer_class(*args, **kwargs)
