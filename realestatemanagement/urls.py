from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Real Estate API",
        default_version="v1",
        description="Test description",
        contact=openapi.Contact(email="thousithouseef731@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("superadmin/", include("superadmin.api.urls")),
    path("tenants/", include("tenants.api.urls")),
    path("accounts/", include("accounts.api.urls")),
    # Swagger API Documentation
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
