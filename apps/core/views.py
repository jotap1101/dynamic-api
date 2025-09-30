from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from apps.core.utils import get_dynamic_model
from apps.core.serializers import get_dynamic_serializer


# Create your views here.
class DynamicModelViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for dynamically selected models.
    The model is determined by the 'model' query parameter in the request.
    """

    def initial(self, request, *args, **kwargs):
        self.db_name = kwargs.get("db_name", "default")
        self.model_name = kwargs.get("model_name")

        if self.db_name not in settings.ALLOWED_DATABASES:
            raise PermissionDenied(detail=f"Database '{self.db_name}' is not allowed.")
        
        if not self.model_name:
            raise ParseError(detail="Model name must be provided as a query parameter.")
        
        try:
            self.model = get_dynamic_model(self.model_name)
        except LookupError as e:
            raise NotFound(detail=str(e))
        except Exception as e:
            raise ParseError(detail=f"Error retrieving model '{self.model_name}': {str(e)}")
        
        self.serializer_class = get_dynamic_serializer(self.model)

        super().initial(request, *args, **kwargs)
    
    def get_queryset(self):
        try:
            return self.model.objects.using(self.db_name).all()
        except Exception as e:
            raise Exception(f"Error accessing database '{self.db_name}': {str(e)}")
        
    def perform_create(self, serializer):
        serializer.save(using=self.db_name)

    def perform_update(self, serializer):
        serializer.save(using=self.db_name)

    def perform_destroy(self, instance):
        instance.delete(using=self.db_name)

    @action(detail=False, methods=['get'])
    def list_models(self, request, *args, **kwargs):
        """
        List all allowed models.
        """
        return Response({"allowed_models": list(settings.ALLOWED_MODELS.keys())})
    
    @action(detail=False, methods=['get'])
    def list_databases(self, request, *args, **kwargs):
        """
        List all allowed databases.
        """
    @action(detail=False, methods=['get'])
    def list_models(self, request):
        """
        List all allowed models.
        """
        return Response({"allowed_models": list(settings.ALLOWED_MODELS.keys())})
    
    @action(detail=False, methods=['get'])
    def list_databases(self, request):
        """
        List all allowed databases.
        """
        return Response({"allowed_databases": settings.ALLOWED_DATABASES})