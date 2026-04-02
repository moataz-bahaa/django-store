from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Collection, Product
from .seralizers import CollectionSeralizer, ProductSerailzer


@api_view(["GET", "POST"])
def produt_list(request):
    if request.method == "GET":
        produts = Product.objects.select_related("collection").all()
        serialzier = ProductSerailzer(produts, many=True, context={"request": request})
        return Response(serialzier.data)
    elif request.method == "POST":
        serialzier = ProductSerailzer(data=request.data)
        serialzier.is_valid(raise_exception=True)
        serialzier.save()
        return Response(serialzier.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    print('product.orderitem_set.count()', product.order_items.count())
    if request.method == "GET":
        serializer = ProductSerailzer(product, context={"request": request})
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProductSerailzer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        if product.order_items.count() > 0:
            return Response(
                {
                    "error": "Product can not be deleted because it is associatd with an order item"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def collection_detail(request, pk):
    collection = Collection.objects.get(pk=pk)
    seralizer = CollectionSeralizer(collection)
    return Response(seralizer.data)
