from rest_framework import serializers
from ..models import User
from django.contrib.auth import password_validation
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# Serializer for Tenant Registeration
class RegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "phone_number",
            "password",
            "password2",
        )

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        # Django builtin password validation that are already configured in settings.py [AUTH_PASSWORD_VALIDATORS]
        password_validation.validate_password(password, self.Meta.model())
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password Doesn't Match"
            )
        return attrs



# Customized Token Claims to identify the tenant for frontend developers
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["username"] = user.username
        token["fullname"] = user.get_full_name()
        return token