from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Collection, Product
from .seralizers import CollectionSeralizer, ProductSerailzer


@api_view()
def produt_list(request):
    produts = Product.objects.select_related("collection").all()
    serialzier = ProductSerailzer(produts, many=True, context={"request": request})
    return Response(serialzier.data)


@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerailzer(product, context={"request": request})
    return Response(serializer.data)


@api_view()
def collection_detail(request, pk):
    collection = Collection.objects.get(pk=pk)
    seralizer = CollectionSeralizer(collection)
    return Response(seralizer.data)
