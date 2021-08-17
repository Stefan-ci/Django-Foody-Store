from django.db.models.signals import post_save
from django.contrib.auth.models import User
from notifications.signals import notify
from products.models import Item




def ping_admins(sender, instance, created, **kwargs):
	verb_msg = "New item added"
	if created:
		if instance.is_public:
			desc = f"""
			Item's name: {instance.title},
			Item's price: ${instance.price},
			item's category: {instance.category},
			Item's access URL: {instance.get_absolute_url}
			"""
			notify.send(instance, 
				recipient=User.objects.filter(is_superuser=True), 
				verb=verb_msg,
				level='info',
				description=desc)
post_save.connect(ping_admins, sender=Item)






