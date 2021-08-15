from django.db import models

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

	class Meta:
		ordering = ('-date', 'amount',)
		get_latest_by = ('date')
		verbose_name = 'Sale'
		verbose_name_plural = 'Sales'

	def __str__(self):
		return str(self.amount)


	def get_total_sale_amount(self):
		total = 0
		for item in self.amount:
			total += item
		return total

