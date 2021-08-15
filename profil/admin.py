from profil.models import Profil
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

class ProfilAdmin(ImportExportModelAdmin):
	fieldsets = []
	list_display = ['user', 'stripe_customer_id', 'one_click_purchasing', 
		'date']
	list_filter = ['date', 'one_click_purchasing']
	search_fields = ['user__username', 'date', 'stripe_customer_id', 
		'one_click_purchasing']


admin.site.register(Profil, ProfilAdmin)
