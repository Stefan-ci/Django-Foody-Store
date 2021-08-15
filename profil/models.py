from django.db import models
from orders.models import OrderItem
from django.contrib.auth.models import User

class Profil(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	stripe_customer_id = models.CharField(max_length=50, blank=True, 
		null=True, verbose_name='Stripe ID')
	one_click_purchasing = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username

	def cart_item_count(self):
		items_count = OrderItem.objects.filter(
			user=self.user,
			ordered=False,
		).count()
		return items_count


