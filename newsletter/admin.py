from django.contrib import admin
from newsletter.models import Newsletter
from import_export.admin import ImportExportModelAdmin

class NewsletterAdmin(ImportExportModelAdmin):
	list_display = ['email', 'date']
	list_filter = ['date']

admin.site.register(Newsletter, NewsletterAdmin)
