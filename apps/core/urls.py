from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DynamicModelViewSet

router = DefaultRouter()

# Registramos com parâmetros dinâmicos (não padrão do DRF Router)
dynamic_list = DynamicModelViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
dynamic_detail = DynamicModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path("<str:db_name>/<str:table_name>/", dynamic_list, name="dynamic-list"),
    path("<str:db_name>/<str:table_name>/<int:pk>/", dynamic_detail, name="dynamic-detail"),
    path("<str:db_name>/<str:table_name>/count/", DynamicModelViewSet.as_view({'get': 'count'}), name="dynamic-count"),
]
