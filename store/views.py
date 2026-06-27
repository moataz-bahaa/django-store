from django.db.models import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import ProductFilter
from .models import Collection, OrderItem, Product, Review
from .seralizers import CollectionSeralizer, ProductSerailzer, ReviewSerazlier
from .pagination import DefaultPagination


class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerailzer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]
    pagination_class = DefaultPagination
    # filterset_fields = ['collection_id', 'unit_price']
    filterset_class = ProductFilter
    

    def get_serializer_context(self):
        return {"context": self.request}

    def destory(self, request, *args, **kwargs):
        if OrderItem.objects.filter(porduct_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "Product can not be deleted because it is associatd with an order item"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(self, request, *args, **kwargs)


class ReviewViewset(ModelViewSet):
    serializer_class = ReviewSerazlier

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}


class CollectionViewset(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSeralizer

    def destory(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response(
                {
                    "error": "Can not delete collection because it includes one or more products"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
