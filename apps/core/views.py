from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.core.serializers import DynamicModelSerializer
from apps.core.utils import get_database_for_model, get_model_from_path


@extend_schema_view(
    list=extend_schema(
        summary="List objects",
        description="Retrieve a list of objects from the specified database and model.",
        tags=["Dynamic API"],
    ),
    create=extend_schema(
        summary="Create object",
        description="Create a new object in the specified database and model.",
        tags=["Dynamic API"],
    ),
    retrieve=extend_schema(
        summary="Get object",
        description="Retrieve a specific object by ID from the specified database and model.",
        tags=["Dynamic API"],
    ),
    update=extend_schema(
        summary="Update object",
        description="Update all fields of a specific object in the specified database and model.",
        tags=["Dynamic API"],
    ),
    partial_update=extend_schema(
        summary="Partial update object",
        description="Update specific fields of an object in the specified database and model.",
        tags=["Dynamic API"],
    ),
    destroy=extend_schema(
        summary="Delete object",
        description="Delete a specific object from the specified database and model.",
        tags=["Dynamic API"],
    ),
)
class DynamicModelViewSet(viewsets.ModelViewSet):
    """
    Dynamic API ViewSet for accessing any model in any configured database.

    URL Pattern: /api/v1/{database}/{model}/

    Parameters:
    - database: Name of the target database (e.g., 'default', 'db1', 'db2', 'db3')
    - model: Name of the model to access (e.g., 'user', 'category', 'product')

    Features:
    - Automatic model detection from URL parameters
    - Database routing based on model and database name
    - Full CRUD operations support
    - JWT authentication required

    Examples:
    - GET /api/v1/db1/product/ - List all products from db1
    - POST /api/v1/db2/animal/ - Create new animal in db2
    - GET /api/v1/db3/movie/123/ - Get specific movie from db3
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

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        context["database"] = self.kwargs.get("database")
        return context

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        database = self.kwargs.get("database")
        model = get_model_from_path(database, self.kwargs.get("model"))
        kwargs["model"] = model
        kwargs["database"] = database
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)
