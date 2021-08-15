from django.urls import path
from django.conf.urls import url
from superadmin import views

urlpatterns = [
	path('', views.admin_home_view, name='admin-home'),
	path('tables/orders/', views.orders_list_view, name='order-table'),


	path('inbox/', views.admin_inbox_view, name='admin-inbox'),
	path('delete/notifications/all/', views.mark_all_as_delete, name='mark_all_notifs_as_delete'),
]
