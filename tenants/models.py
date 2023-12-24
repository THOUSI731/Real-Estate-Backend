from django.db import models
from accounts.models import User
from properties.models import Unit
# Create your models here.

class Profile(models.Model):
     tenant=models.OneToOneField(User,related_name="tenant_profile",on_delete=models.CASCADE)
     profile_picture=models.ImageField(upload_to="user_profile",null=True)
     address=models.CharField(max_length=100)
     city=models.CharField(max_length=50)
     state=models.CharField(max_length=50)
     state=models.CharField(max_length=50)
     pin_code=models.CharField(max_length=20)    
     
     def __str__(self) -> str:
          return self.tenant.first_name    
     
class TenantDocument(models.Model):
     tenant=models.ForeignKey(User,related_name="tenant_documents",on_delete=models.CASCADE)
     document_name=models.CharField(max_length=100)
     document_number=models.CharField(max_length=100)
     document_image=models.ImageField(upload_to="tenant_documents")
     upload_date=models.DateTimeField(auto_now_add=True)
     
     def __str__(self) -> str:
          return self.tenant.first_name
     
class TenantAgreement(models.Model):
     tenant=models.ForeignKey(User,on_delete=models.CASCADE,related_name="tenant_agreements")
     unit=models.ForeignKey(Unit,on_delete=models.CASCADE,related_name="tenant_agreement_units")  
     start_date=models.DateField()
     end_date=models.DateField()      
     monthly_rent_date=models.DateField()   
     
     def __str__(self) -> str:
          return f"{self.tenant.first_name} - {self.unit.property_reference.name} - {self.unit.unit_type}"
                                                                                                                                                                                      




     
