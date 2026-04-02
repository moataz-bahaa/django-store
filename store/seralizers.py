from decimal import Decimal

from rest_framework import serializers

from .models import Collection, Product


class CollectionSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title"]


class ProductSerailzer(serializers.ModelSerializer):

    class Meta:
        model = Product
        # fields = "__all__"
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "inventory",
            "unit_price",
            "collection",
        ]
        read_only_fields = ["slug"]
