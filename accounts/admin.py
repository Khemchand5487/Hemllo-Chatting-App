from django.contrib import admin
from accounts.models import Accounts, OTP

# Register your models here.
admin.site.register(Accounts)
admin.site.register(OTP)
