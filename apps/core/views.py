from typing import Any, Dict
import logging

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
        name="db",
        description="Nome do banco de dados (ex: 'default', 'db1', 'db2', 'db3')",
        required=True,
        type=str,
        location=OpenApiParameter.QUERY,
        enum=["default", "db1", "db2", "db3"],
    ),
    OpenApiParameter(
        name="table",
        description="Nome da tabela a ser acessada (ex: 'category', 'product')",
        required=True,
        type=str,
        location=OpenApiParameter.QUERY,
    ),
]

# Parâmetros de paginação
pagination_parameters = [
    OpenApiParameter(
        name="page",
        description="Número da página a ser retornada",
        required=False,
        type=int,
        location=OpenApiParameter.QUERY,
        default=1,
    ),
    OpenApiParameter(
        name="page_size",
        description="Número de registros por página (máx: 100)",
        required=False,
        type=int,
        location=OpenApiParameter.QUERY,
        default=10,
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
        description=(
            "Retrieve a paginated list of objects from the specified database and model. "
            "Use 'page' parameter to navigate through pages and 'page_size' to control "
            "the number of items per page (max: 100)."
        ),
        parameters=common_parameters + pagination_parameters,
        tags=["Dynamic API"],
        responses={
            200: inline_serializer(
                name="DynamicListResponse",
                fields={
                    "count": serializers.IntegerField(
                        help_text="Total number of items"
                    ),
                    "next": serializers.URLField(
                        help_text="URL for next page", allow_null=True
                    ),
                    "previous": serializers.URLField(
                        help_text="URL for previous page", allow_null=True
                    ),
                    "results": serializers.ListField(
                        child=serializers.JSONField(help_text="Object data"),
                        help_text="List of objects matching the query",
                    ),
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

    URL Pattern: /api/v1/

    Required Query Parameters:
    - db: Name of the target database (e.g., 'default', 'db1', 'db2', 'db3')
    - table: Name of the table/model to access (e.g., 'user', 'category', 'product')

    Features:
    - Automatic model detection from query parameters
    - Database routing based on model and database name
    - Full CRUD operations support
    - JWT authentication required
    - Consistent error handling for missing parameters

    Examples:
    - GET /api/v1/?db=db1&table=product - List all products from db1
    - POST /api/v1/?db=db2&table=animal - Create new animal in db2
    - GET /api/v1/123/?db=db3&table=movie - Get specific movie from db3
    - PUT /api/v1/123/?db=db1&table=product - Update product in db1
    - DELETE /api/v1/123/?db=db2&table=animal - Delete animal in db2

    Error Responses:
    - 400 Bad Request: When 'db' or 'table' parameters are missing
    - 404 Not Found: When database or model doesn't exist
    - 401 Unauthorized: When authentication is missing or invalid
    """

    permission_classes = [IsAuthenticated]
    serializer_class = DynamicModelSerializer
    lookup_field = "id"

    def initial(self, request, *args, **kwargs):
        """
        Runs before any other action.
        Validates required query parameters.
        """
        super().initial(request, *args, **kwargs)

        # Collect all validation errors
        errors = {}
        if not request.query_params.get("db"):
            errors["db"] = "Database parameter is required"
        if not request.query_params.get("table"):
            errors["table"] = "Table parameter is required"

        # Raise validation error with all missing parameters
        if errors:
            raise ValidationError(errors)

    def get_queryset(self):
        """
        Get the list of items for this view.
        Determines the appropriate database and model from query parameters.
        """

        try:
            # Obtém os parâmetros da query string
            database_name = self.request.query_params.get("db")
            model_name = self.request.query_params.get("table")

            # Get model class based on URL parameters
            model = get_model_from_path(database_name, model_name)

            # Validate and get correct database
            db = get_database_for_model(model, database_name)

            # Return ordered queryset using the appropriate database
            return model.objects.using(db).all().order_by("id")
        except NotFound as e:
            import logging
            logging.error(f"NotFound exception in get_queryset: {e}")
            raise NotFound("The requested resource was not found.")
        except Exception as e:
            import logging, traceback
            logging.error(f"Error accessing {model_name} in database {database_name}.\n{traceback.format_exc()}")
            raise NotFound("An internal error occurred while accessing the requested data.")

    def get_serializer_context(self) -> Dict[str, Any]:
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        context["database"] = self.request.query_params.get("db", "default")
        return context

    def get_serializer(self, *args: Any, **kwargs: Any) -> DynamicModelSerializer:
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """

        serializer_class = self.get_serializer_class()
        database = self.request.query_params.get("db")
        model_name = self.request.query_params.get("table")

        # Get model class based on URL parameters
        model = get_model_from_path(database, model_name)
        kwargs["model"] = model
        kwargs["database"] = database
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)
