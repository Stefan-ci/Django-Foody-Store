from django.contrib import admin
from refunds.models import Refund
from import_export.admin import ImportExportModelAdmin

class RefundAdmin(ImportExportModelAdmin):
	list_display = ['reason', 'accepted', 'email', 'date']
	list_filter = ['date', 'accepted']

	date_hierarchy = 'date'

	def has_delete_permission(self, request, obj=None):
		return False

	def has_change_permission(self, request, obj=None):
		return False


admin.site.register(Refund, RefundAdmin)

