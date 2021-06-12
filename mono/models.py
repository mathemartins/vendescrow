from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class AccountLinkage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=299, blank=True, null=True)
    mono_code = models.CharField(max_length=299, blank=True, null=True)
    exchange_token = models.CharField(max_length=299, blank=True, null=True)

    email = models.CharField(max_length=300, blank=True, null=True)
    phone = models.CharField(max_length=300, blank=True, null=True)
    gender = models.CharField(max_length=300, blank=True, null=True)

    bvn = models.CharField(max_length=300, blank=True, null=True)
    marital_status = models.CharField(max_length=300, blank=True, null=True)
    home_address = models.CharField(max_length=300, blank=True, null=True)
    office_address = models.CharField(max_length=300, blank=True, null=True)

    bank = models.CharField(max_length=300, blank=True, null=True)
    account_number = models.CharField(max_length=300, blank=True, null=True)
    account_type = models.CharField(max_length=300, blank=True, null=True)
    currency = models.CharField(max_length=300, blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "account_linkage"
        verbose_name = "Account Linkage"
        verbose_name_plural = "Accounts Linkage"

    def __str__(self):
        return str(self.user.username)
