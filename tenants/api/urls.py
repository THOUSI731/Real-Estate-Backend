from django.urls import path
from .. import views

urlpatterns = [
    path("test/",views.test,name="test"),
    path("profile/",views.TenantProfileGetUpdateAPIView.as_view(),name="tenant-get-update")
]
