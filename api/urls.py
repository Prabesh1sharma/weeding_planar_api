from django.urls import path

from .views import recommend_wedding_planners
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Wedding Planners API",
        default_version='v1',
        description="API documentation for the Wedding Planners project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('recommend/', recommend_wedding_planners, name='recommend_wedding_planners'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]