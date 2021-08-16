from django.contrib import admin
from contacts.models import Contact
from import_export.admin import ImportExportModelAdmin

class ContactAdmin(ImportExportModelAdmin):
	list_display = ['name', 'email', 'subject', 'is_answered', 'date']
	list_filter = ['email', 'date', 'is_answered']
	date_hierarchy = 'date'

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def has_change_permission(self, request, obj=None):
		return False


admin.site.register(Contact, ContactAdmin)
