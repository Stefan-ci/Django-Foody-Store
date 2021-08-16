from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
	path('', views.apiOverview),
	path('items/list/', views.itemsList),
	path('item/detail/<int:pk>/', views.itemDetail),
]
