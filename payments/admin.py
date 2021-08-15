from django.contrib import admin
from payments.models import Payment
from import_export.admin import ImportExportModelAdmin


class PaymentAdmin(ImportExportModelAdmin):
	list_display = ['user', 'stripe_charge_id', 'amount', 'date']
	list_filter = ['date']
	search_fields = ['user__username', 'stripe_charge_id', 'amount', 'date']

admin.site.register(Payment, PaymentAdmin)