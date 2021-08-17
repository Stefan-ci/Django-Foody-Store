from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
	name = models.CharField(max_length=150)
	email = models.EmailField()
	subject = models.CharField(max_length=100)
	message = models.TextField(null=True)
	date = models.DateTimeField(auto_now_add=True)
	is_answered = models.BooleanField(default=False)
	unread = models.BooleanField(default=True)
	deleted = models.BooleanField(default=False)

	
	def __str__(self):
		return str(self.email)

