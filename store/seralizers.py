from decimal import Decimal

from rest_framework import serializers

from .models import Collection, Product


class CollectionSeralizer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)


class ProductSerailzer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(
        source="unit_price", max_digits=6, decimal_places=2
    )
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all()
    # )
    collection = serializers.StringRelatedField()

    collection_name=serializers.StringRelatedField(
        source='collection'
    )
    # collection = CollectionSeralizer()
    collection_obj = CollectionSeralizer(source='collection')
    collection_url = serializers.HyperlinkedRelatedField(
        source='collection',
        queryset=Collection.objects.all(),
        view_name="collection-detail"
    )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
