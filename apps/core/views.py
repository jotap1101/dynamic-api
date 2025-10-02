from typing import Any, Dict

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers, viewsets
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated

from apps.core.serializers import DynamicModelSerializer
from apps.core.utils import get_database_for_model, get_model_from_path

# Parâmetros comuns para todas as operações
common_parameters = [
    OpenApiParameter(
        name="database",
        description="Nome do banco de dados (ex: 'default', 'db1', 'db2', 'db3')",
        required=True,
        type=str,
        location=OpenApiParameter.PATH,
        enum=["default", "db1", "db2", "db3"],
    ),
    OpenApiParameter(
        name="model",
        description="Nome do modelo a ser acessado (ex: 'category', 'product')",
        required=True,
        type=str,
        location=OpenApiParameter.PATH,
    ),
]

# Parâmetro ID para operações que precisam dele
id_parameter = OpenApiParameter(
    name="id",
    description="UUID do objeto",
    required=True,
    type=OpenApiTypes.UUID,
    location=OpenApiParameter.PATH,
)


@extend_schema_view(
    list=extend_schema(
        summary="List objects",
        description="Retrieve a list of objects from the specified database and model.",
        parameters=common_parameters,
        tags=["Dynamic API"],
        responses={
            200: inline_serializer(
                name="DynamicListResponse",
                fields={
                    "results": serializers.ListField(child=serializers.DictField())
                },
            )
        },
    ),
    create=extend_schema(
        summary="Create object",
        description="Create a new object in the specified database and model.",
        parameters=common_parameters,
        tags=["Dynamic API"],
        request=inline_serializer(
            name="DynamicCreateRequest",
            fields={"data": serializers.DictField()},
        ),
        responses={
            201: inline_serializer(
                name="DynamicCreateResponse",
                fields={"data": serializers.DictField()},
            )
        },
    ),
    retrieve=extend_schema(
        summary="Get object",
        operation_id="dynamic_retrieve",
        description="Retrieve a specific object by ID from the specified database and model.",
        parameters=common_parameters + [id_parameter],
        tags=["Dynamic API"],
        responses={
            200: inline_serializer(
                name="DynamicRetrieveResponse",
                fields={"data": serializers.DictField()},
            )
        },
    ),
    update=extend_schema(
        summary="Update object",
        description="Update all fields of a specific object in the specified database and model.",
        parameters=common_parameters + [id_parameter],
        tags=["Dynamic API"],
        request=inline_serializer(
            name="DynamicUpdateRequest",
            fields={"data": serializers.DictField()},
        ),
        responses={
            200: inline_serializer(
                name="DynamicUpdateResponse",
                fields={"data": serializers.DictField()},
            )
        },
    ),
    partial_update=extend_schema(
        summary="Partial update object",
        description="Update specific fields of an object in the specified database and model.",
        parameters=common_parameters + [id_parameter],
        tags=["Dynamic API"],
        request=inline_serializer(
            name="DynamicPatchRequest",
            fields={"data": serializers.DictField()},
        ),
        responses={
            200: inline_serializer(
                name="DynamicPatchResponse",
                fields={"data": serializers.DictField()},
            )
        },
    ),
    destroy=extend_schema(
        summary="Delete object",
        description="Delete a specific object from the specified database and model.",
        parameters=common_parameters + [id_parameter],
        tags=["Dynamic API"],
        responses={204: None},
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
    lookup_field = "id"

    def get_queryset(self):
        """
        Get the list of items for this view.
        Determines the appropriate database and model from the URL.
        """

        try:
            database_name = self.kwargs.get("database", "default")
            model_name = self.kwargs.get("model")

            if not model_name:
                raise ValidationError("Model name is required")

            # Get model class based on URL parameters
            model = get_model_from_path(database_name, model_name)

            # Validate and get correct database
            db = get_database_for_model(model, database_name)

            # Return queryset using the appropriate database
            return model.objects.using(db).all()
        except NotFound as e:
            raise NotFound(str(e))
        except Exception as e:
            raise NotFound(
                f"Error accessing {model_name} in database {database_name}: {str(e)}"
            )

    def get_serializer_context(self) -> Dict[str, Any]:
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        context["database"] = self.kwargs.get("database", "default")
        return context

    def get_serializer(self, *args: Any, **kwargs: Any) -> DynamicModelSerializer:
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """

        serializer_class = self.get_serializer_class()
        database = self.kwargs.get("database", "default")
        model_name = self.kwargs.get("model")

        if not model_name:
            raise ValidationError("Model name is required")

        # Get model class based on URL parameters
        model = get_model_from_path(database, model_name)
        kwargs["model"] = model
        kwargs["database"] = database
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)
