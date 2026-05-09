from decimal import Decimal

from rest_framework import serializers

from .models import Collection, Product, Review


class CollectionSeralizer(serializers.ModelSerializer):
    products_count = serializers.ReadOnlyField()

    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]


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


class ReviewSerazlier(serializers.ModelSerializer):

    def create(self, validated_data):
        print('context', self.context)
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    
    class Meta:
        model = Review
        fields = ['id', 'name', 'description']
