from django.db.models.signals import post_save
from django.contrib.auth.models import User
from notifications.signals import notify
from payments.models import Payment




def ping_admins(sender, instance, created, **kwargs):
	verb_msg = "There is a new payment"
	if created:
		desc = f"""
		Payment made by: {instance.user.username} ({instance.user.email})
		Payment amount: ${instance.amount},
		Payment date: {instance.date},
		Charge id: {instance.stripe_charge_id}
		"""
		notify.send(instance, 
			recipient=User.objects.filter(is_superuser=True), 
			verb=verb_msg,
			level='info',
			description=desc)
post_save.connect(ping_admins, sender=Payment)






