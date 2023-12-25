from django.urls import path
from .. import views

urlpatterns = [
    path("",views.PropertyListCreateAPIView.as_view(),name="property-list-create"),
    path("<int:pk>/",views.PropertyDetailUpdateAPIView.as_view(),name="property-list-create"),
    path("<int:pk>/unit/",views.PropertyUnitCreateAPIView.as_view(),name="property-list-create"),
    path("<int:pk>/unit/<int:unit_pk>/",views.PropertyUnitDetailAPIView.as_view(),name="property-list-create"),
]
