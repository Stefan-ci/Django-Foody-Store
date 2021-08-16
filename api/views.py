from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic.detail import SingleObjectMixin
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view
from rest_framework.response import Response



from products.models import Item
from .serializers import ItemSerializer





@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'List' : '/item-list/',
		'Detail view' : '/item-detail/<str:pk>/',
	}
	return Response(api_urls)



@api_view(['GET'])
def itemsList(request):
	try:
		items = Item.objects.all()
		serializer = ItemSerializer(items, many=True)
		return Response(serializer.data)
	except:
		return Response(None)



@api_view(['GET'])
def itemDetail(request, pk):
	try:
		item = Item.objects.get(id=pk)
		serializer = ItemSerializer(item, many=False)
		return Response(serializer.data)
	except ObjectDoesNotExist:
		return Response(None)
