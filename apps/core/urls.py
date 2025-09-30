from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.core.views import DynamicModelViewSet

router = DefaultRouter()

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
    path('<str:db_name>/<str:model_name>/', dynamic_list, name='dynamic-list'),
    path('<str:db_name>/<str:model_name>/<int:pk>/', dynamic_detail, name='dynamic-detail'),
    path('list-models/', DynamicModelViewSet.as_view({'get': 'list_models'}), name='list-models'),
    path('list-databases/', DynamicModelViewSet.as_view({'get': 'list_databases'}), name='list-databases'),
]