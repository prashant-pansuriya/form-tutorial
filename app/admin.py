from django.contrib import admin

""" admin register """
from .models import CustomerInquiry, OTP

admin.site.register(CustomerInquiry)
admin.site.register(OTP)
