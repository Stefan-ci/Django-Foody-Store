from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from notifications.signals import notify
from profil.models import Profil


def create_profile(sender, instance, created, **kwargs):
	if created:
		try:
			group = Group.objects.get(name='public')
			if group:
				instance.groups.add(group)
		except:
			pass
		Profil.objects.create(user=instance)
		print(f'Profil created: {instance.username}')
post_save.connect(create_profile, sender=User)





def ping_admins(sender, instance, created, **kwargs):
	verb_msg = "Registration"
	desc = f"There is a new user. Username: {instance.username}. Email: {instance.email}."
	if created:
		notify.send(instance, 
			recipient=User.objects.filter(is_superuser=True), 
			verb=verb_msg,
			level='info',
			description=desc)
post_save.connect(ping_admins, sender=User)




