from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .api.serializers import (
    PropertyPOSTSerializer,
    PropertyGETSerializer,
    PropertyProfileGETSerializer,
    UnitPOSTSerializer,
    PropertyUnitGETSerializer,
    TenantAgreementPOSTSerializer,
    TenantGETProfileSerializer,
)
from rest_framework import status
from properties.models import Property, Unit, Feature
from .pagination import SmallResultPagination
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.models import User
from tenants.api.serializers import TenantGETSerializer
from tenants.models import TenantAgreement
from django.db.models import Q


@api_view(["GET"])
def test(request):
    return Response("Success")


# 2.2.Property Listing Module
class PropertyListCreateAPIView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)

    # Here Listing All the Properties of SuperAdmin means Admin
    def get(self, request):
        search = request.GET.get("search", None)
        Q_obj_filter = Q()
        if search:
            Q_obj_filter |= Q(features__name__istartswith=search)
        queryset = Property.objects.prefetch_related("features").filter(Q_obj_filter)
        # created pagination to reduce load time
        paginator = SmallResultPagination()
        paginated_data = paginator.paginate_queryset(queryset, request)
        serializer = PropertyGETSerializer(paginated_data, many=True)
        response_data = {
            "total_page": paginator.page.paginator.num_pages,
            "property": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    # Here Creating New Properties
    def post(self, request):
        serializer = PropertyPOSTSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        property_ = Property.objects.create(
            name=serializer.validated_data.get("property_name", None),
            property_type=serializer.validated_data.get("property_type", None),
            address=serializer.validated_data.get("address", None),
            city=serializer.validated_data.get("city", None),
            state=serializer.validated_data.get("state", None),
            country=serializer.validated_data.get("country", None),
            pin_code=serializer.validated_data.get("pin_code", None),
        )
        # Features is a many to many Field
        features = serializer.validated_data.get("features", None)
        if features is not None:
            features_data = [
                Feature.objects.get_or_create(name=feature)[0] for feature in features
            ]
            property_.features.add(*features_data)
            property_.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PropertyDetailUpdateAPIView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)

    # For PUT and Delete Operation
    def get_property_object_or_404(self, id):
        try:
            return Property.objects.get(pk=id)
        except:
            raise NotFound({"data": "Property Not Found"})

    permission_classes = (AllowAny,)

    def get(self, request, pk=None):
        search = request.GET.get("search", None)
        Q_obj_base = Q(id=pk)
        Q_obj_filter=Q()
        if search:
            Q_obj_filter |= Q(property_units__features__name__istartswith=search)
            Q_obj_base &= Q_obj_filter
        # property profile view with units and assigned tenant information
        try:
            instance = Property.objects.prefetch_related(
                "property_units__tenant_agreement_units__tenant", "features"
            ).filter(Q_obj_base)
        except:
            return Response(
                {"data": "Property Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Nested Serializer
        serializer = PropertyProfileGETSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        instance = self.get_property_object_or_404(id=pk)
        serializer = PropertyPOSTSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        instance.name = serializer.validated_data.get("property_name", instance.name)
        instance.property_type = serializer.validated_data.get(
            "property_type", instance.property_type
        )
        instance.address = serializer.validated_data.get("address", instance.address)
        instance.city = serializer.validated_data.get("city", instance.city)
        instance.state = serializer.validated_data.get("state", instance.state)
        instance.country = serializer.validated_data.get("country", instance.country)
        instance.pin_code = serializer.validated_data.get("pin_code", instance.pin_code)
        features = serializer.validated_data.get("features", instance.features)
        features_data = [
            Feature.objects.get_or_create(name=feature)[0] for feature in features
        ]
        instance.features.set(features_data)
        instance.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        instance = self.get_property_object_or_404(pk)
        instance.delete()
        return Response(
            {"data": "Property Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class PropertyUnitCreateAPIView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)

    # Here the pk is refered to the property id
    # cause based on property i am creating property unit Property (One) to (Many) Property Unit
    def post(self, request, pk=None):
        serializer = UnitPOSTSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        property_ = get_object_or_404(Property, id=pk)
        unit = Unit.objects.create(
            property_reference=property_,
            unit_type=serializer.validated_data.get("unit_type", None),
            rent_cost=serializer.validated_data.get("rent_cost", None),
            unit_status=serializer.validated_data.get("unit_status", None),
        )
        features = serializer.validated_data.get("features", None)
        if features is not None:
            features_data = [
                Feature.objects.get_or_create(name=feature)[0] for feature in features
            ]
            unit.features.add(*features_data)
            unit.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PropertyUnitDetailAPIView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)

    # In this class the url path is like property/<int:pk>/unit/<int:unit_pk>/
    def get(self, request, unit_pk=None, *args, **kwargs):
        try:
            instance = Unit.objects.prefetch_related(
                "tenant_agreement_units__tenant", "features"
            ).get(id=unit_pk)
        except:
            return Response(
                {"data": "Property Unit is not Found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = PropertyUnitGETSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, unit_pk=None, *args, **kwargs):
        instance = get_object_or_404(Unit, id=unit_pk)
        serializer = UnitPOSTSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        instance.unit_type = serializer.validated_data.get(
            "unit_type", instance.unit_type
        )
        instance.rent_cost = serializer.validated_data.get(
            "rent_cost", instance.rent_cost
        )
        instance.unit_type = serializer.validated_data.get(
            "unit_status", instance.unit_status
        )
        features = serializer.validated_data.get("features", instance.features)
        features_data = [
            Feature.objects.get_or_create(name=feature)[0] for feature in features
        ]
        instance.features.set(features_data)
        instance.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, unit_pk=None, *args, **kwargs):
        instance = get_object_or_404(Unit, id=unit_pk)
        instance.delete()
        return Response(
            {"data": "Property Unit Deleted Successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class TenantListAPIView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(is_tenant=True).select_related("tenant_profile")
        paginator = SmallResultPagination()
        paginated_data = paginator.paginate_queryset(queryset, request)
        serializer = TenantGETSerializer(paginated_data, many=True)
        response_data = {
            "total_page": paginator.page.paginator.num_pages,
            "tenants": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class TenantAgreementCreateAPIView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)

    # Assign a tenant with a unit under a property with details like agreement end date, monthly rent date.
    # Here pk refers to the Unit
    def get(self, request, pk=None, *args, **kwargs):
        serializer = TenantAgreementPOSTSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        tenant_email = serializer.validated_data.get("tenant", None)
        tenant = get_object_or_404(User, email=tenant_email)
        unit = get_object_or_404(Unit, id=pk)
        tenant_agreement = TenantAgreement.objects.create(
            tenant=tenant,
            unit=unit,
            start_date=serializer.validated_data.get("start_date", None),
            end_date=serializer.validated_data.get("end_date", None),
            monthly_rent_date=serializer.validated_data.get("monthly_rent_date", None),
        )
        # Add feature like
        # Sending Mail As Notificarion to the User(Tenant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Show tenant profile view with personal information and rental information
class TenantProfileDetailView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_tenant_object_or_404(self, id):
        try:
            return User.objects.select_related("tenant_profile").prefetch_related(
                "tenant_agreements"
            )
        except:
            raise NotFound("Tenant Not Found")

    def get(self, request, pk=None):
        instance = self.get_tenant_object_or_404(pk)
        serializer = TenantGETProfileSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
