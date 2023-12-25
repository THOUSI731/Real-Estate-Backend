from rest_framework import serializers
from properties.models import Property, Unit, Feature
from tenants.api.serializers import TenantAgreementSerializer
from tenants.models import TenantAgreement
from accounts.models import User
from tenants.models import TenantDocument


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
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Pin code Must Be 6 digit number")
        return value

    def validate_features(self, value):
        return [tag.title() for tag in value]

    def validate_property_type(self, value):
        return value.lower()


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ("id", "name")


class PropertyGETSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True)

    class Meta:
        model = Property
        fields = (
            "id",
            "name",
            "property_type",
            "features",
        )
        read_only_fields = ("id",)


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
    features = serializers.ListField(
        child=serializers.CharField(min_length=5, max_length=50)
    )

    class Meta:
        model = Unit
        fields = ("unit_type", "rent_cost", "unit_status", "features")

    def validate_features(self, value):
        return [tag.title() for tag in value]

    def unit_type(self, value):
        return value.lower()

    def unit_status(self, value):
        return value.lower()


class TenantAgreementPOSTSerializer(serializers.ModelSerializer):
    tenant = serializers.EmailField(max_length=50)

    class Meta:
        model = TenantAgreement
        fields = ("tenant", "start_date", "end_date", "monthly_rent_date")

    # Frontend Input is Like Date with Time so i splitted with "T" part and takes the first dat that is date
    def validate_start_date(self, value):
        return value.split("T")[0]

    def validate_end_date(self, value):
        return value.split("T")[0]

    def validate_monthly_rent_date(self, value):
        return value.split("T")[0]


from tenants.api.serializers import TenantProfileSerializer


class TenantAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantAgreement
        fields = ("id", "start_date", "end_date", "monthly_rent_date")


class TenantDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantDocument
        fields = ("document_name", "document_number")


class TenantGETProfileSerializer(serializers.ModelSerializer):
    profile = TenantProfileSerializer(source="tenant_profile")
    documents = TenantDocumentSerializer(source="tenant_documents",many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "profile",
            "documents",
        )
