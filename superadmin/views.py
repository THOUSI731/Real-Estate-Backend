from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .api.serializers import (
    PropertyPOSTSerializer,
    PropertyGETSerializer,
    PropertyProfileGETSerializer,
    UnitPOSTSerializer,
    PropertyUnitGETSerializer,
)
from rest_framework import status
from properties.models import Property, Unit, Feature
from .pagination import SmallResultPagination
from django.shortcuts import get_object_or_404


@api_view(["GET"])
def test(request):
    return Response("Success")


# 2.2.Property Listing Module
class PropertyListCreateAPIView(APIView):
    # Here Listing All the Properties of SuperAdmin means Admin
    def get(self, request):
        queryset = Property.objects.all()
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
            property_.save(update_fields=["features"])
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PropertyDetailUpdateAPIView(APIView):
    # For PUT and Delete Operation
    def get_property_object_or_404(self, id):
        try:
            return Property.objects.get(pk=id)
        except:
            raise Response(
                {"data": "Property Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, pk=None):
        # property profile view with units and assigned tenant information
        try:
            instance = Property.objects.prefetch_related(
                "property_units__tenant_agreement_units__tenant","features"
            ).get(pk=id)
        except:
            raise Response(
                {"data": "Property Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Nested Serializer
        serializer = PropertyProfileGETSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        instance = self.get_property_object_or_404(pk=id)
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
    # Here the id is refered to the property 
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
            property_.features.add(*features_data)
            property_.save(update_fields=["features"])
            unit.features.add(*features_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PropertyUnitDetailAPIView(APIView):
    def get(self, request, pk=None):
        try:
            instance = Unit.objects.prefetch_related("tenant_agreement_units__tenant","features").get(id=pk)
        except:
            return Response({"data":"Property Unit is not Found"},status=status.HTTP_404_NOT_FOUND)
        serializer = PropertyUnitGETSerializer(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)
        

    def put(self, request, pk=None):
        instance = get_object_or_404(Unit, id=pk)
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

    def delete(self, request, pk=None):
        instance = get_object_or_404(Unit, id=pk)
        instance.delete()
        return Response(
            {"data": "Property Unit Deleted Successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
