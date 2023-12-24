from rest_framework import serializers
from properties.models import Property, Unit, Feature
from tenants.api.serializers import TenantAgreementSerializer


class PropertyPOSTSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(max_length=50)
    features = serializers.ListField(
        child=serializers.CharField(min_length=5, max_length=50)
    )

    class Meta:
        model = Property
        fields = (
            "property_name",
            "property_type",
            "address",
            "city",
            "state",
            "country",
            "pin_code",
            "features",
        )

    def validate_pin_code(self, value):
        if not value.is_digit() or len(value) != 6:
            raise serializers.ValidationError("Pin code Must Be 6 digit number")
        return value

    def validate_features(self, value):
        return [tag.title() for tag in value]

    def validate_property_type(self, value):
        return value.lower()


class PropertyGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            "id",
            "name",
            "property_type",
            "features",
        )
        read_only_fields = ("id",)


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ("id", "name")


class PropertyUnitGETSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)
    # TenantAgreementSerializer from tenants.api.serializers
    tenant_agreements = TenantAgreementSerializer(read_only=True)

    class Meta:
        model = Unit
        fields = (
            "id",
            "unit_type",
            "rent_cost",
            "features",
            "unit_status",
            "tenant_agreements",
        )
        read_only_fields = ("id",)


class PropertyProfileGETSerializer(serializers.ModelSerializer):
    property_units = PropertyUnitGETSerializer(many=True, read_only=True)
    features = FeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = (
            "id",
            "property_type",
            "address",
            "city",
            "state",
            "country",
            "pin_code",
            "features",
            "property_units",
        )

class UnitPOSTSerializer(serializers.ModelSerializer):
    features=serializers.ListField(child=serializers.CharField(min_length=5,max_length=50))
    
    class Meta:
        model=Unit
        fields=("unit_type","rent_cost","unit_status","features")
        
    def validate_features(self, value):
        return [tag.title() for tag in value]
    
    def unit_type(self,value):
        return value.lower()
    
    def unit_status(self,value):
        return value.lower()

        
        
    