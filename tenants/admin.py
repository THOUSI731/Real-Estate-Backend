from django.contrib import admin
from .models import TenantAgreement, TenantDocument, Profile

admin.site.register(TenantAgreement)
admin.site.register(TenantDocument)
admin.site.register(Profile)
