from django.db.models.signals import post_save
from django.contrib.auth.models import User
from notifications.signals import notify
from orders.models import Order




def ping_admins(sender, instance, created, **kwargs):
	verb_msg = "New order"
	if created:
		if instance.ordered:
			desc = f"There is a new order. Date: {instance.ordered_date}"
			notify.send(instance, 
				recipient=User.objects.filter(is_superuser=True), 
				verb=verb_msg,
				level='success',
				description=desc)
post_save.connect(ping_admins, sender=Order)






