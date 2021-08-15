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
		print(f'Profil créé avec succès: {instance.username}')
post_save.connect(create_profile, sender=User)





def ping_admins(sender, instance, created, **kwargs):
	verb_msg = f"{instance.username} s'est inscrit !"
	desc = f"""
	Son adresse mail est {instance.email}.
	"""
	if created:
		notify.send(instance, 
			recipient=User.objects.filter(is_superuser=True), 
			verb=verb_msg,
			level='info',
			description=desc)
post_save.connect(ping_admins, sender=User)






def send_welcome_notif(sender, instance, created, **kwargs):
	verb_msg = f"Soyez la bienvenue cher/chère {instance.username}!"
	
	desc = f"""Pour rappel, votre email est: {instance.email}, votre nom d'utilisateur est: {instance.username} 
	et le mot de passe est celui que vous avez renseigné lors de votre inscription. Ne l'oubliez surtout pas.
	Cependant vous pouvez toujours le réinitialiser en accédant à la page de connexion!

	Heureux de vous compter parmi nous!
	"""

	if created:
		notify.send(instance, 
			recipient=instance, 
			verb=verb_msg,
			level='success',
			description=desc)
post_save.connect(send_welcome_notif, sender=User)





