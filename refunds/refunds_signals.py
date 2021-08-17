from django.db.models.signals import post_save
from django.contrib.auth.models import User
from notifications.signals import notify
from refunds.models import Refund




def ping_admins(sender, instance, created, **kwargs):
	verb_msg = "There is a new refund request"
	if created:
		desc = f"""
		Request made by: {instance.order.user.username} ({instance.email})
		Refund date: {instance.date},
		Reason: {instance.reason}
		"""
		notify.send(instance, 
			recipient=User.objects.filter(is_superuser=True), 
			verb=verb_msg,
			level='error',
			description=desc)
post_save.connect(ping_admins, sender=Refund)






