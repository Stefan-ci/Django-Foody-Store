from django.contrib import admin
from newsletter.models import Newsletter
from import_export.admin import ImportExportModelAdmin

class NewsletterAdmin(ImportExportModelAdmin):
	list_display = ['email', 'date']
	list_filter = ['date']

	date_hierarchy = 'date'

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def has_change_permission(self, request, obj=None):
		return False

admin.site.register(Newsletter, NewsletterAdmin)
