from django.db import models

class Coupon(models.Model):
	code = models.CharField(max_length=50)
	amount = models.FloatField()
	date = models.DateTimeField(auto_now_add=True)
	end_date = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=False)

	def __str__(self):
		return self.code
