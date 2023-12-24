from django.urls import path
from .. import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("test/", views.test, name="test"),
    path(
        "register/",
        views.TenantRegisterationAPIView.as_view(),
        name="tenant-registeration-view",
    ),
    path("login/", views.UserLoginAPIView.as_view(), name="user-login"),
    path("token/refresh/", TokenRefreshView.as_view(),name="user-token-refresh"),
]
