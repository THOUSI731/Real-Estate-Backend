from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .api.serializers import RegisterationSerializer, MyTokenObtainPairSerializer
from rest_framework import status
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView


@api_view(["GET"])
def test(request):
    return Response("Test Success")


class TenantRegisterationAPIView(APIView):  
    def post(self, request):
        serializer = RegisterationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(
            first_name=serializer.validated_data.get("first_name", None),
            last_name=serializer.validated_data.get("last_name", None),
            email=serializer.validated_data.get("email", None),
            phone_number=serializer.validated_data.get("phone_number", None),
            username=serializer.validated_data.get("username", None),
            is_tenant=True
        )
        user.set_password(serializer.validated_data.get("password"))
        user.save(update_fields=["password"])
        # created signals for creating tenant profile instance
        return Response(
            {"data":"Tenant Registered Successfully"}, status=status.HTTP_201_CREATED
        )

    
# for tenant and user login apiview
class UserLoginAPIView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer