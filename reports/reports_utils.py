from reports.models import Sales, Expenses
from django.db.models import Sum


def sales_made():
	total_sales_amount = 0
	total_sales_amount_dict = Sales.objects.aggregate(Sum('amount'))
	total_sales_amount = total_sales_amount_dict['amount__sum']
	if total_sales_amount is None:
		total_sales_amount = 0
	return total_sales_amount


def expenses_made():
	total_expenses_amount = 0
	total_expenses_amount_dict = Expenses.objects.aggregate(Sum('amount'))
	total_expenses_amount = total_expenses_amount_dict['amount__sum']
	if total_expenses_amount is None:
		total_expenses_amount = 0
	return total_expenses_amount



def monthly_sales(month):
	month = int(month)
	monthly_sales_amount = 0
	monthly_sales_amount_dict = Sales.objects.filter(date__month=month).aggregate(Sum('amount'))
	monthly_sales_amount = monthly_sales_amount_dict['amount__sum']
	if monthly_sales_amount is None:
		monthly_sales_amount = 0
	return monthly_sales_amount


def monthly_expenses(month):
	month = int(month)
	monthly_expenses_amount = 0
	monthly_expenses_amount_dict = Expenses.objects.filter(date__month=month).aggregate(Sum('amount'))
	monthly_expenses_amount = monthly_expenses_amount_dict['amount__sum']
	if monthly_expenses_amount is None:
		monthly_expenses_amount = 0
	return monthly_expenses_amount






