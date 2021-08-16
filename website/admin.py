from import_export.admin import ImportExportModelAdmin
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

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def has_change_permission(self, request, obj=None):
		return False

	"""
		Add custom actions to Model `User`
	"""
	def activate_user(self, request, queryset):
		updated = queryset.update(is_active=True)
		self.message_user(request, ngettext(
				"%d user successfully activated",
				"%d users successfully activated",
				updated,
			) % updated, messages.SUCCESS)
	text = 'Activate selected users'
	activate_user.short_description = text



	def deactivate_user(self, request, queryset):
		updated = queryset.update(is_active=False)
		self.message_user(request, ngettext(
				"%d user successfully deactivated",
				"%d users successfully deactivated",
				updated,
			) % updated, messages.SUCCESS)
	text = "Deactivate selected users"
	deactivate_user.short_description = text



	def make_user_staff(self, request, queryset):
		updated = queryset.update(is_staff=True)
		self.message_user(request, ngettext(
				"%d user successfully promoted to staff",
				"%d users successfully promoted to staff",
				updated,
			) % updated, messages.SUCCESS)
	text = "Promote selected users"
	make_user_staff.short_description = text



	def remove_user_staff(self, request, queryset):
		updated = queryset.update(is_staff=False)
		self.message_user(request, ngettext(
				"%d user is no more staff",
				"%d users are no more staff",
				updated,
			) % updated, messages.SUCCESS)
	text = "Deprive selected users"
	remove_user_staff.short_description = text





admin.site.site_header = "Django Administration | Foody "
admin.site.index_title = "Administration 1 😋😋 | Foody "
admin.site.enable_nav_sidebar = True


admin.site.unregister(User)
admin.site.register(User, UserCustomAdmin)
