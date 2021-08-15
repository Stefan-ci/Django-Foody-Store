from django.db import models


class Newsletter(models.Model):
	email = models.EmailField(unique=True)
	date = models.DateTimeField(auto_now_add=True)

	

	def __str__(self):
		return str(self.email)
