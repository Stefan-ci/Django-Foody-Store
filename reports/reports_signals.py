from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from notifications.signals import notify
from reports.models import Sales, Expenses
from orders.models import Order, OrderItem
from payments.models import Payment



def create_sale_report(sender, instance, created, **kwargs):
	if created:
		Sales.objects.create(
			amount=instance.amount,
			sale_type="Sale (order)",
			reason="There is a new sale (payment) on the store",
		)
		print(f'New sale made by: {instance.user.username}')
post_save.connect(create_sale_report, sender=Payment)




