from rest_framework import serializers
from ..models import User,TenantAgreement
class TenantGETSerializer(serializers.ModelSerializer):
    full_name=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=("full_name","email","phone_number")
    
    def get_full_name(self,obj):
        return f"{obj.first_name} {obj.last_name}"
    
class TenantAgreementSerializer(serializers.ModelSerializer):
    tenant=TenantGETSerializer(read_only=True)
    class Meta:
        model=TenantAgreement
        fields=("tenant","start_date","end_date","monthly_rent_date")