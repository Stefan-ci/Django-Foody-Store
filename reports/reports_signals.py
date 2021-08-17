from django.contrib.auth.models import User
from django.db.models.signals import post_save
from notifications.signals import notify
from reports.models import Sales, Expenses
from orders.models import Order, OrderItem
from payments.models import Payment



def create_sale_report(sender, instance, created, **kwargs):
	if created:
		Sales.objects.create(
			amount=instance.amount,
			payment_id=instance.id,
			sale_type="Sale (order)",
			payment_charge_id=instance.stripe_charge_id,
			reason="There is a new sale (payment) on the store",
		)
post_save.connect(create_sale_report, sender=Payment)




def sales_ping_admins(sender, instance, created, **kwargs):
	verb_msg = "New item added"
	if created:
		desc = f"""
		Sale amount: ${instance.amount},
		Sale type: {instance.sale_type},
		Sale reason: {instance.reason},
		Sale date: {instance.date},
		"""
		notify.send(instance, 
			recipient=User.objects.filter(is_superuser=True), 
			verb=verb_msg,
			level='success',
			description=desc)
post_save.connect(sales_ping_admins, sender=Sales)




def expenses_ping_admins(sender, instance, created, **kwargs):
	verb_msg = "New expense"
	if created:
		desc = f"""
		Expense amount: ${instance.amount},
		Expense type: {instance.sale_type},
		Expense reason: {instance.reason},
		Expense date: {instance.date},
		"""
		notify.send(instance, 
			recipient=User.objects.filter(is_superuser=True), 
			verb=verb_msg,
			level='error',
			description=desc)
post_save.connect(expenses_ping_admins, sender=Expenses)


