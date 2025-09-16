from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import render

from store.models import Collection, Order, OrderItem, Product


def say_hello(request):
    # query_set = Product.objects.all() # query set are lazy
    # build a complix query that will be evalutated later when iterating over items/using list/accessing specific item by it's index
    # query_set.filter().filter().order_by()

    # count = Product.objects.count()
    # product = Product.objects.get(pk=0)
    # product = Product.objects.filter(pk=0).first() # if list is empty first() returns None
    # product = Product.objects.filter(pk=0).exists() # returns a boolean

    # queryset = Product.objects.filter(unit_price__gte=20)
    # queryset = Product.objects.filter(unit_price__range=(20, 30))

    # queryset = Product.objects.filter(collection__id__gte=2)
    # queryset = Product.objects.filter(collection__id__range=(1, 2))
    # queryset = Product.objects.filter(title__contains='coffee') # case sensitive
    # queryset = Product.objects.filter(title__icontains="coffee")

    # queryset = Product.objects.filter(last_update__year=2021)
    # queryset = Product.objects.filter(description__isnull=True)
    # queryset = Collection.objects.filter(featured_product__isnull=True)
    # queryset = Order.objects.filter(customer__id=1)
    # queryset = Product.objects.filter(inventory__lt=2)
    # queryset = OrderItem.objects.filter(product__collection__id=3)

    # queryset = Product.objects.filter(inventory__lt=20, unit_price__lt=20)
    # queryset = Product.objects.filter(inventory__lt=20).filter(unit_price__lt=20)

    # OR
    # queryset = Product.objects.filter(Q(inventory__lt=20) | Q(unit_price__lt=20))
    # queryset = Product.objects.filter(Q(inventory__lt=20) & Q(unit_price__lt=20))
    # ~ = not operator in sql
    # queryset = Product.objects.filter(~Q(unit_price__lt=20))

    # to refrece a a field
    # queryset = Product.objects.filter(inventory=F('unit_price'))
    # queryset = Product.objects.filter(inventory=F('collection__id'))

    # Sorting
    # queryset = Product.objects.order_by("title")
    # queryset = Product.objects.order_by("-title")
    # queryset = Product.objects.order_by("title", "-unit_price")
    # queryset = Product.objects.order_by("title", "-unit_price").reverse()
    # queryset = Product.objects.filter(collection_id=1).order_by("unit_price")
    # queryset = Product.objects.order_by("unit_price")
    # product = queryset[0] # get the first element

    # product = Product.objects.earliest('unit_price') # order by unit_price and get the first element
    # product = Product.objects.latest('unit_price')

    # limiting results (pagination)
    # queryset = Product.objects.all()[:5]
    # queryset = Product.objects.all()[5:10]

    # Seleting only specified columns
    # queryset = Product.objects.values("id", "title")
    # queryset = Product.objects.values("id", "title", "collection__title") # returns a dict {'id': 2}
    # queryset = Product.objects.values_list("id", "title", "collection__title") # returns a tuble

    # fetching producgts that have been ordered
    # queryset = Product.objects.filter(
    #     id__in=OrderItem.objects.values("product_id").distinct()
    # ).order_by("title")

    # if you tried to access product.unit_price (field that doesn't exist in only), it will run sql for each product to selec the unit_price
    # queryset = Product.objects.only('id', 'title')

    # exclude description field
    # queryset = Product.objects.defer("description")

    # Joins
    # we use select_related when 1 instance exist - product has one collection
    # queryset = Product.objects.select_related('collection').all()
    # prefetch_related (n)
    # queryset = Product.objects.prefetch_related("promotions").all()

    # queryset = (
    #     Product.objects.prefetch_related("promotions")
    #     .select_related("collection")
    #     .all()
    # )

    queryset = (
        Order.objects.select_related("customer")
        .prefetch_related("orderitem_set")
        .order_by("-placed_at")[:5]
    )

    return render(request, "hello.html", {"name": "moataz", "orders": queryset})
