from django.urls import path
from django.conf.urls import url
from superadmin import views

urlpatterns = [
	path('', views.admin_home_view, name='admin-home'),


	path('orders/all/', views.all_orders_list_view, name='all-orders'),
	path('orders/order_detail/<int:id>/', views.order_detail_view, name='order-detail'),
	path('orders/not-received/', views.not_received_orders_list_view, name='order-not-received'),
	path('orders/not-delivered/', views.not_delivered_orders_list_view, name='order-not-delivered'),

	path('inbox/', views.admin_inbox_view, name='admin-inbox'),
	

	path('messages/new_messages/', views.new_messages_list_view, name='new-messages'),


	# Custom actions (no need templates)
	path('delete/notifications/all/', views.mark_all_as_delete, name='mark_all_notifs_as_delete'),
	path('mark-as-delivered/<int:id>/', views.mark_as_delivered, name='mark_as_delivered'),
	path('mark-as-received/<int:id>/', views.mark_as_received, name='mark_as_received'),

	path('mark-message-as-deleted/<int:id>/', views.mark_contact_as_deleted, name='mark_msg_as_deleted'),
	path('mark-message-as-read/<int:id>/', views.mark_contact_as_read, name='mark_msg_as_read_and_answered'),

]
