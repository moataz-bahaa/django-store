from django.contrib import admin, messages
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode

from . import models


class ProductInventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [("<10", "Low")]

    def queryset(self, request, queryset):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):  # also fixed typo
    actions = ["clear_inventory"]
    list_display = [
        "id",
        "title",
        "unit_price",
        "inventory_status",
        # "collection", # string represnetation for colleciton
        "collection_title",
    ]
    list_filter = ["collection", "last_update", ProductInventoryFilter]
    list_editable = ["unit_price"]
    list_per_page = 10
    list_select_related = ["collection"]
    search_fields = ["title"]

    # customozing form
    # fields=['title', 'slug']
    # exclude=['promotions']
    # readonly_fields=['title']
    prepopulated_fields = {"slug": ["title"]}
    autocomplete_fields = ["collection"]

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "OK"

    def collection_title(self, product):
        return product.collection.title

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} produts were successfully updated",
            messages.SUCCESS,
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "email", "phone", "membership"]
    list_editable = ["membership"]
    ordering = ["first_name", "last_name"]
    search_fields = ["first_name__istartswith", "last_name__istartswith"]
    list_per_page = 10


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ["product"]
    model = models.OrderItem
    extra = 0
    min_num = 1
    max_num = 10


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer"]
    list_display = ["id", "customer", "payment_status", "placed_at"]
    list_editable = ["payment_status"]
    inlines = [OrderItemInline]
    list_per_page = 10


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "products_count"]
    search_fields = ["title"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        # return format_html('<a href="https://google.com">{}</a>', collection.products_count)
        # return collection.products_count

        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode(
                {
                    "collectoin__id": str(collection.id),
                }
            )
        )

        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("product"))
