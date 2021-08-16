from django.contrib import admin
from payments.models import Payment
from import_export.admin import ImportExportModelAdmin


class PaymentAdmin(ImportExportModelAdmin):
	list_display = ['user', 'stripe_charge_id', 'amount', 'date']
	list_filter = ['date']
	search_fields = ['user__username', 'stripe_charge_id', 'amount', 'date']
	date_hierarchy = 'date'

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def has_change_permission(self, request, obj=None):
		return False

admin.site.register(Payment, PaymentAdmin)