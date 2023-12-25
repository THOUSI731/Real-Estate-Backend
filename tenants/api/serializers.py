from rest_framework import serializers
from ..models import Profile, TenantAgreement, TenantDocument
from accounts.models import User


class TenantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("profile_picture", "address", "city", "state", "country", "pin_code")


class TenantDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantDocument
        fields = ("document_name", "document_number", "document_image", "upload_date")


class TenantGETSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    profile = TenantProfileSerializer(source="tenant_profile")
    documents = TenantDocumentsSerializer(source="tenant_documents", many=True)

    class Meta:
        model = User
        fields = ("id", "full_name", "email", "phone_number", "profile", "documents")

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class TenantAgreementSerializer(serializers.ModelSerializer):
    tenant = TenantGETSerializer(read_only=True)

    class Meta:
        model = TenantAgreement
        fields = ("tenant", "start_date", "end_date", "monthly_rent_date")


class TenantProfilePOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("profile_picture", "address", "city", "state", "country", "pin_code")

    def validate_pin_code(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Pin code Must Be 6 digit number")
        return value


class TenantDocumentPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantDocument
        fields = ("document_name", "document_number", "document_image")


class TenantPOSTSerializer(serializers.ModelSerializer):
    profile = TenantProfilePOSTSerializer(source="tenant_profile")
    email = serializers.EmailField()
    username = serializers.CharField()
    phone_number = serializers.CharField()
    documents = TenantDocumentPOSTSerializer(source="tenant_documents")

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "phone_number",
            "profile",
            "documents",
        )

    def validate_email(self, value):
        if self.instance:
            if User.objects.exclude(id=self.instance.id).filter(email=value).exists():
                raise serializers.ValidationError(
                    {"email": "This email is already in use"}
                )
            return value

    def validate_username(self, value):
        if self.instance:
            if (
                User.objects.exclude(id=self.instance.id)
                .filter(username=value)
                .exists()
            ):
                raise serializers.ValidationError(
                    {"username": "This Username is already in use"}
                )
            return value

    def validate_phone_number(self, value):
        if self.instance:
            if (
                User.objects.exclude(id=self.instance.id)
                .filter(phone_number=value)
                .exists()
            ):
                raise serializers.ValidationError(
                    {"phone_number": "This Phone Number is already in use"}
                )
            return value

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        documents_data = validated_data.pop("documents", {})
        if profile_data:
            tenant_profile_serializer = TenantProfilePOSTSerializer(
                instance=self.instance.tenant_profile, data=profile_data
            )
            serializers.is_valid(raise_exception=True)
            self.instance.tenant_profile.profile_picture = (
                tenant_profile_serializer.validated_data.get(
                    "profile_picture", self.instance.tenant_profile.profile_picture
                )
            )
            self.instance.tenant_profile.address = (
                tenant_profile_serializer.validated_data.get(
                    "address", self.instance.tenant_profile.address
                )
            )
            self.instance.tenant_profile.city = (
                tenant_profile_serializer.validated_data.get(
                    "city", self.instance.tenant_profile.city
                )
            )
            self.instance.tenant_profile.state = (
                tenant_profile_serializer.validated_data.get(
                    "state", self.instance.tenant_profile.state
                )
            )
            self.instance.tenant_profile.country = (
                tenant_profile_serializer.validated_data.get(
                    "country", self.instance.tenant_profile.country
                )
            )
            self.instance.tenant_profile.pin_code = (
                tenant_profile_serializer.validated_data.get(
                    "pin_code", self.instance.tenant_profile.pin_code
                )
            )
            self.instance.tenant_profile.save()
        return instance
