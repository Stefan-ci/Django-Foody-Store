from django.contrib import admin
from reports.models import Sales, Expenses
from import_export.admin import ImportExportModelAdmin




class SalesAdmin(ImportExportModelAdmin):
	list_display = ['amount', 'sale_type', 'reason', 'date']
	list_filter = ['date']
	search_fields = ['amount', 'sale_type', 'reason', 'date']
	date_hierarchy = 'date'

	def __init__(self, *args, **kwargs):
		super(SalesAdmin, self).__init__(*args, **kwargs)
		self.list_display_links = None

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request):
		return False





class ExpensesAdmin(ImportExportModelAdmin):
	list_display = ['amount', 'expense_type', 'reason', 'date']
	list_filter = ['date']
	search_fields = ['amount', 'expense_type', 'reason', 'date']




admin.site.register(Sales, SalesAdmin)
admin.site.register(Expenses, ExpensesAdmin)
