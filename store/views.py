from django.db.models import Count
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


@api_view(["GET", "POST"])
def collection_list(request):
    if request.method == "GET":
        queryset = Collection.objects.annotate(products_count=Count("products")).all()
        serialzier = CollectionSeralizer(queryset, many=True)
        return Response(serialzier.data)
    elif request.method == "POST":
        serialzier = CollectionSeralizer(data=request.data)
        serialzier.is_valid(raise_exception=True)
        serialzier.save()
        return Response(serialzier.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if request.method == "GET":
        seralizer = CollectionSeralizer(collection)
        return Response(seralizer.data)
    elif request.method == "PUT":
        seralizer = CollectionSeralizer(collection, data=request.data)
        seralizer.is_valid(raise_exception=True)
        seralizer.save()
        return Response(seralizer.data)
    elif request.method == "DELETE":
        if collection.products.count() > 0:
            return Response(
                {
                    "error": "Can not delete collection because it includes one or more products"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
