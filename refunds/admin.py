from django.contrib import admin
from refunds.models import Refund
from import_export.admin import ImportExportModelAdmin

class RefundAdmin(ImportExportModelAdmin):
	list_display = ['reason', 'accepted', 'email', 'date']
	list_filter = ['date', 'accepted']


admin.site.register(Refund, RefundAdmin)

