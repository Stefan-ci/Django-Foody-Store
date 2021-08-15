from import_export.admin import ImportExportModelAdmin
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from django.contrib.auth.models import User
from django.contrib import admin, messages




class UserCustomAdmin(ImportExportModelAdmin):
	list_display = ['username', 'email', 'is_active', 'is_staff', 
		'is_superuser', 'date_joined']
	list_filter = ['is_active', 'is_staff', 'is_superuser']
	ordering = ['-id']
	search_fields = ['first_name', 'last_name', 'username', 'date_joined']
	actions = ['activate_user', 'deactivate_user', 'make_user_staff', 
	'remove_user_staff']


	"""
		Add custom actions to Model `User`
	"""
	def activate_user(self, request, queryset):
		updated = queryset.update(is_active=True)
		self.message_user(request, ngettext(
				"%d utilisateur a bien été activé",
				"%d utilisateurs ont bien été activés",
				updated,
			) % updated, messages.SUCCESS)
	text = _("Activer les utilisateurs sélectionnés")
	activate_user.short_description = text



	def deactivate_user(self, request, queryset):
		updated = queryset.update(is_active=False)
		self.message_user(request, ngettext(
				"%d utilisateur a bien été désactivé",
				"%d utilisateurs ont bien été désactivés",
				updated,
			) % updated, messages.SUCCESS)
	text = _("Désactiver les utilisateurs sélectionnés")
	deactivate_user.short_description = text



	def make_user_staff(self, request, queryset):
		updated = queryset.update(is_staff=True)
		self.message_user(request, ngettext(
				"%d utilisateur a bien été promu 'AUXILIAIRE' ",
				"%d utilisateurs ont bien été promus 'AUXILIAIRES'",
				updated,
			) % updated, messages.SUCCESS)
	text = _("Promouvoir les utilisateurs sélectionnés")
	make_user_staff.short_description = text



	def remove_user_staff(self, request, queryset):
		updated = queryset.update(is_staff=False)
		self.message_user(request, ngettext(
				"%d utilisateur n'est plus 'AUXILIAIRE' ",
				"%d utilisateurs ne sont plus 'AUXILIAIRES'",
				updated,
			) % updated, messages.SUCCESS)
	text = _("Déchoir les utilisateurs sélectionnés")
	remove_user_staff.short_description = text





admin.site.site_header = _("Site d'administration de Django | Food !")
admin.site.index_title = _("Administration 1 😋😋 | Food")
admin.site.enable_nav_sidebar = True


admin.site.unregister(User)
admin.site.register(User, UserCustomAdmin)
