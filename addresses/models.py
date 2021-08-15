from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Address(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	street_address = models.CharField(max_length=100, verbose_name='Rue')
	apartment_address = models.CharField(max_length=100, 
		verbose_name='Appartement')
	country = CountryField(multiple=False, verbose_name='Pays')
	zip = models.CharField(max_length=100, verbose_name='Code postal')
	address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES, 
		verbose_name="Type d'adresse")
	default = models.BooleanField(default=False, 
		verbose_name='Adresse par défaut')

	def __str__(self):
		return self.user.username

	class Meta:
		verbose_name = 'Adresse'
		verbose_name_plural = 'Adresses'
