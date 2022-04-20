""" model file """
from django.db import models
import uuid


class CustomerInquiry(models.Model):
    """customer inquiry"""

    customer_name = models.CharField(max_length=30, verbose_name="Customer Name")
    email_id = models.EmailField(verbose_name="Email Id")
    phone_no = models.CharField(max_length=60, verbose_name="Phone No")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    complaint_msg = models.TextField(
        verbose_name="Customer Complaint Message", max_length=230
    )
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """return string"""
        return self.name


class OTP(models.Model):
    """otp model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    mobile_no = models.CharField(max_length=10, default="7202844636")
    otp = models.CharField(max_length=100)
    expire_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """return string"""
        return str(self.otp)
