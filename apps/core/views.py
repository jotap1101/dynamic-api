from django.conf import settings
from django.db import OperationalError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import get_dynamic_serializer
from .utils import get_dynamic_model


class DynamicModelViewSet(ModelViewSet):
    """
    ViewSet genérico que acessa dinamicamente um banco e uma tabela.
    """

    def initial(self, request, *args, **kwargs):
        self.db_name = kwargs.get("db_name")
        self.table_name = kwargs.get("table_name")

        # valida banco
        if self.db_name not in settings.ALLOWED_DATABASES:
            self.permission_denied(
                request, message=f"Banco '{self.db_name}' não permitido."
            )

        # valida model
        try:
            self.model = get_dynamic_model(self.table_name)
        except LookupError as e:
            self.permission_denied(request, message=str(e))

        self.serializer_class = get_dynamic_serializer(self.model)
        return super().initial(request, *args, **kwargs)

    def get_queryset(self):
        try:
            return self.model.objects.using(self.db_name).all()
        except OperationalError:
            # tabela não existe no banco

            raise NotFound(
                detail=f"Tabela '{self.table_name}' não existe no banco '{self.db_name}'. "
                f"Verifique se as migrations foram aplicadas."
            )
        except Exception as e:
            # erro inesperado
            from rest_framework.exceptions import APIException

            raise APIException(detail=str(e))

    def perform_create(self, serializer):
        try:
            serializer.save(using=self.db_name)
        except OperationalError:
            raise NotFound(
                detail=f"Não foi possível criar: tabela '{self.table_name}' "
                f"não existe no banco '{self.db_name}'."
            )

    def perform_update(self, serializer):
        try:
            serializer.save(using=self.db_name)
        except OperationalError:
            raise NotFound(
                detail=f"Não foi possível atualizar: tabela '{self.table_name}' "
                f"não existe no banco '{self.db_name}'."
            )

    def perform_destroy(self, instance):
        try:
            instance.delete(using=self.db_name)
        except OperationalError:
            raise NotFound(
                detail=f"Não foi possível excluir: tabela '{self.table_name}' "
                f"não existe no banco '{self.db_name}'."
            )

    @action(detail=False, methods=["get"])
    def count(self, request, *args, **kwargs):
        try:
            count = self.get_queryset().count()
            return Response({"table": self.table_name, "count": count})
        except OperationalError:
            return Response(
                {
                    "error": f"Tabela '{self.table_name}' não existe no banco '{self.db_name}'."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
