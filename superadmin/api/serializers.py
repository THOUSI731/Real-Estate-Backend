from rest_framework import serializers
from properties.models import Property, Unit, Feature
from tenants.models import TenantAgreement
from accounts.models import User
from tenants.models import TenantDocument
from tenants.api.serializers import TenantGETSerializer


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
            "property_image",
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
    property_image = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = (
            "id",
            "name",
            "property_type",
            "property_image",
            "features",
        )
        read_only_fields = ("id",)

    def get_property_image(self, obj):
        base_url = "http://127.0.0.1:8000"
        return f"{base_url + obj.property_image.url}"


class TenantAgreementSerializer(serializers.ModelSerializer):
    tenant = TenantGETSerializer(read_only=True)

    class Meta:
        model = TenantAgreement
        fields = ("id", "start_date", "end_date", "monthly_rent_date","tenant")


class PropertyUnitGETSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)
    tenant_agreements = TenantAgreementSerializer(read_only=True,many=True,source="tenant_agreement_units")

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
    property_image = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = (
            "id",
            "name",
            "property_image",
            "property_type",
            "address",
            "city",
            "state",
            "country",
            "pin_code",
            "features",
            "property_units",
        )

    def get_property_image(self, obj):
        print(obj.property_image.url)
        base_url = "http://127.0.0.1:8000"
        return f"{base_url + obj.property_image.url}"


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


class TenantDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantDocument
        fields = ("document_name", "document_number")


class TenantGETProfileSerializer(serializers.ModelSerializer):
    profile = TenantProfileSerializer(source="tenant_profile")
    documents = TenantDocumentSerializer(source="tenant_documents", many=True)

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
