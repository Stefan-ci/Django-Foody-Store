from django.db import models
from payments.models import Payment

class Expenses(models.Model):
	amount = models.FloatField(null=True, blank=True)
	date = models.DateTimeField(auto_now_add=True)
	expense_type = models.CharField(max_length=200)
	reason = models.TextField()

	class Meta:
		verbose_name = 'Expense'
		verbose_name_plural = 'Expenses'

	def __str__(self):
		return str(self.amount)




class Sales(models.Model):
	amount = models.FloatField(null=True, blank=True, editable=False)
	date = models.DateTimeField(auto_now_add=True, editable=False)
	sale_type = models.CharField(max_length=200, editable=False)
	reason = models.TextField(editable=False)
	payment_id = models.ForeignKey(Payment, on_delete=models.DO_NOTHING,
		null=True, blank=True)
	payment_charge_id = models.ForeignKey(Payment,null=True,blank=True,
		related_name='charge_id',on_delete=models.DO_NOTHING)

	class Meta:
		ordering = ('-date', 'amount',)
		get_latest_by = ('date')
		verbose_name = 'Sale'
		verbose_name_plural = 'Sales'

	def __str__(self):
		return str(self.amount)

