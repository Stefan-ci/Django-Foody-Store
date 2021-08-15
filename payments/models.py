from django.db import models
from django.contrib.auth.models import User


class Payment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_charge_id = models.CharField(max_length=50, 
        verbose_name='Stripe ID')
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.stripe_charge_id)

