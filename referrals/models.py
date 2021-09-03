from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.

class EarlyBirdAccess(models.Model):
    email = models.EmailField()
    referral_code = models.CharField(max_length=10)
    number_of_referrals = models.IntegerField(default=0)
    base_url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('-number_of_referrals',)
        db_table = 'early_access'
        verbose_name = 'Early Access'
        verbose_name_plural = 'Early Access'


class UserReferrals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_referrals = models.IntegerField(default=0)
    base_url = models.URLField()
    earnings = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    class Meta:
        ordering = ('-number_of_referrals',)
        db_table = 'referrals'
        verbose_name = 'Referrals'
        verbose_name_plural = 'Referrals'
