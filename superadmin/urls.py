from django.urls import path
from django.conf.urls import url
from superadmin import views

urlpatterns = [
	path('', views.admin_home_view, name='admin-home'),
]
