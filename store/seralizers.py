from decimal import Decimal

from rest_framework import serializers

from .models import Collection, Product


class CollectionSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title"]


class ProductSerailzer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        source="unit_price", max_digits=6, decimal_places=2
    )
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    collection_name = serializers.StringRelatedField(source="collection")
    collection = CollectionSeralizer()
    collection_url = serializers.HyperlinkedRelatedField(
        source="collection",
        queryset=Collection.objects.all(),
        view_name="collection-detail",
    )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

    class Meta:
        model = Product
        # fields = "__all__"
        fields = [
            "id",
            "title",
            "collection_name",
            "price",
            "price_with_tax",
            "collection",
            "collection_url",
        ]
