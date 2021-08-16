from website import views
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.home_view, name='home'),
	
	path('add-food-to-cart/<id>/<slug>/', views.add_food_to_cart, name='add-food-to-cart'),
	path('remove-food-from-cart/<id>/<slug>/', views.remove_food_from_cart, name='remove-from-cart'),
	path('remove-single-food-from-cart/<id>/<slug>/', views.remove_single_item_from_cart, name='remove-single-food-from-cart'),
	
	path('order/summary/', views.order_summary_view, name='order-summary'),
	path('order/checkout/', views.CheckoutView.as_view(), name='checkout'),
	path('order/payment/<payment_option>/', views.PaymentView.as_view(), name='payment'),

	path('food/<id>/<slug>/', views.food_item_detail_view, name='food-detail'),
	path('foods/', views.food_item_list_view, name='food-list'),
	path('foods/category/category=<category>/', views.food_category_list_view, name='food-category'),

	path('add-coupon/', views.AddCouponView.as_view(), name='add-coupon'),
	path('request/refund/', views.RequestRefundView.as_view(), name='request-refund'),

	path('user/login/', views.login_view, name='login'),
	path('user/logout/', views.logout_view, name='logout'),
	path('user/register/', views.RegisterView.as_view(), name='register'),

	path('contact-us/', views.contact_us_view, name='contact'),

	path('access/denied/', views.not_allowed_view, name='not-allowed'),


	# Password reset urls
	path('reset/password/', auth_views.PasswordResetView.as_view(template_name='public/password/forgot_form.html'), name="reset_password"), 
	path('reset/password/sent/', auth_views.PasswordResetDoneView.as_view(template_name='public/password/reset_sent.html'), name="password_reset_done"),   
	path('reset/password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='public/password/reset_form.html'), name="password_reset_confirm"), 
	path('reset/password/success/', auth_views.PasswordResetCompleteView.as_view(template_name='public/password/reset_complete.html'), name="password_reset_complete"),






	path('test/', views.change_item_popular_status),
]
