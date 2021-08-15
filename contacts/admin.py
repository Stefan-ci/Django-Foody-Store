from django.contrib import admin
from contacts.models import Contact
from import_export.admin import ImportExportModelAdmin

class ContactAdmin(ImportExportModelAdmin):
	list_display = ['name', 'email', 'subject', 'is_answered', 'date']
	list_filter = ['email', 'date', 'is_answered']


admin.site.register(Contact, ContactAdmin)
