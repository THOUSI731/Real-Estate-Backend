from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from tenants.models import Profile

@receiver(post_save,sender=User)
def create_profile_instance(sender,instance,created,**kwargs):
     if created and instance.is_tenant:
          Profile.objects.create(tenant=instance)
               
          