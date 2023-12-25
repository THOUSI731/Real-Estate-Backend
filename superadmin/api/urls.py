from django.urls import path
from .. import views

urlpatterns = [
    path("", views.PropertyListCreateAPIView.as_view(), name="property-list-create"),
    path(
        "<int:pk>/",
        views.PropertyDetailUpdateAPIView.as_view(),
        name="property-list-create",
    ),
    path(
        "<int:pk>/unit/",
        views.PropertyUnitCreateAPIView.as_view(),
        name="property-list-create",
    ),
    path(
        "<int:pk>/unit/<int:unit_pk>/",
        views.PropertyUnitDetailAPIView.as_view(),
        name="property-list-create",
    ),
    path("tenants/", views.TenantListAPIView.as_view(), name="tenant-list-view"),
    path("tenants/agreement/", views.TenantAgreementCreateAPIView.as_view(), name="tenant-list-view"),
    path("tenants/profile/", views.TenantProfileDetailView.as_view(), name="tenant-list-view"),
]
