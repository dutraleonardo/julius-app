"""Julius_App URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers


router = routers.DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="julius_app API",
        default_version='v1',
        description="API julius_app",
        terms_of_service="https://terms.julius_app.com",
        contact=openapi.Contact(email="contact@julius_app.com"),
        license=openapi.License(name="Copyright"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('julius_app.apps.accounts.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger-ui/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
