from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .api.serializers import TenantGETSerializer,TenantPOSTSerializer
from rest_framework import status
@api_view(["GET"])
def test(request):
     return Response("Test Success")

class TenantProfileGetUpdateAPIView(APIView):
     def get(self,request,format=None):
          serializer=TenantGETSerializer(request.user)
          return Response(serializer.data,status=status.HTTP_200_OK)
     
     def put(self,request,format=None):
          serializer=TenantPOSTSerializer(instance=request.user,data=request.data)
          if not serializer.is_valid():
               return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
          instance=request.user
          instance.first_name=serializer.validated_data.get("first_name",instance.first_name)
          instance.last_name=serializer.validated_data.get("first_name",instance.last_name)
          instance.email=serializer.validated_data.get("first_name",instance.email)
          instance.phone_number=serializer.validated_data.get("first_name",instance.phone_numbet)
          instance.username=serializer.validated_data.get("first_name",instance.username)
          instance.save()
          # Profile Instance Updating
          serializer.save()
          return Response(serializer.data,status=status.HTTP_200_OK)
     
     def delete(self,request,format=None):
          try:
               request.user.delete()
               return Response({"msg":"Account Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)
          except:
               return Response({"msg":"Either Your Account is Deleted Nor You Account is Not Found"},status=status.HTTP_404_NOT_FOUND)
          
     
