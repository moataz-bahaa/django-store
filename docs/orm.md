# 🧠 Django ORM Cheat Sheet — Based on Your `say_hello` Function

This guide summarizes **real-world ORM examples** from your Django course.
Each section shows how to write and understand queries using Django’s ORM (`QuerySet`).

---

## ⚙️ Setup & Imports

```python
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, connection
from django.db.models import (
    Avg, Count, DecimalField, ExpressionWrapper,
    F, Func, Max, Min, Q, Sum, Value
)
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.shortcuts import render

from store.models import Collection, Customer, Order, OrderItem, Product
from tags.models import Tag, TaggedItem
```

---

## 🏁 QuerySet Basics

- **QuerySets are lazy:** they don’t hit the database until evaluated (e.g., when converting to list or iterating).

```python
queryset = Product.objects.all()
```

Chained filters are also lazy:

```python
queryset = Product.objects.filter().filter().order_by()
```

---

## 🔍 Retrieving Data

```python
count = Product.objects.count()
product = Product.objects.get(pk=0)
product = Product.objects.filter(pk=0).first()  # Returns None if not found
exists = Product.objects.filter(pk=0).exists()  # Returns a boolean
```

---

## 🎯 Filtering

### 1. Simple filters

```python
queryset = Product.objects.filter(unit_price__gte=20)
queryset = Product.objects.filter(unit_price__range=(20, 30))
```

### 2. Related field filters

```python
queryset = Product.objects.filter(collection__id__gte=2)
queryset = Product.objects.filter(collection__id__range=(1, 2))
```

### 3. String lookups

```python
queryset = Product.objects.filter(title__contains='coffee')    # Case-sensitive
queryset = Product.objects.filter(title__icontains='coffee')   # Case-insensitive
```

### 4. Date and null filters

```python
queryset = Product.objects.filter(last_update__year=2021)
queryset = Product.objects.filter(description__isnull=True)
queryset = Collection.objects.filter(featured_product__isnull=True)
```

### 5. Relational filters

```python
queryset = Order.objects.filter(customer__id=1)
queryset = Product.objects.filter(inventory__lt=2)
queryset = OrderItem.objects.filter(product__collection__id=3)
```

---

## 🔢 Combining Filters

### AND filters

```python
queryset = Product.objects.filter(inventory__lt=20, unit_price__lt=20)
# OR equivalently:
queryset = Product.objects.filter(inventory__lt=20).filter(unit_price__lt=20)
```

### OR / AND / NOT using `Q`

```python
queryset = Product.objects.filter(Q(inventory__lt=20) | Q(unit_price__lt=20))
queryset = Product.objects.filter(Q(inventory__lt=20) & Q(unit_price__lt=20))
queryset = Product.objects.filter(~Q(unit_price__lt=20))  # NOT
```

---

## ⚖️ Comparing Fields (F expressions)

```python
queryset = Product.objects.filter(inventory=F('unit_price'))
queryset = Product.objects.filter(inventory=F('collection__id'))
```

---

## 📚 Sorting Results

```python
queryset = Product.objects.order_by("title")
queryset = Product.objects.order_by("-title")
queryset = Product.objects.order_by("title", "-unit_price")
queryset = Product.objects.order_by("title", "-unit_price").reverse()
queryset = Product.objects.filter(collection_id=1).order_by("unit_price")

# Get first or last item based on ordering
product = Product.objects.earliest('unit_price')
product = Product.objects.latest('unit_price')
```

---

## ⏳ Limiting (Pagination)

```python
queryset = Product.objects.all()[:5]
queryset = Product.objects.all()[5:10]
```

---

## 🎯 Selecting Specific Fields

```python
queryset = Product.objects.values("id", "title")
queryset = Product.objects.values("id", "title", "collection__title")
queryset = Product.objects.values_list("id", "title", "collection__title")
```

---

## 🛒 Filtering Products That Have Been Ordered

```python
queryset = Product.objects.filter(
    id__in=OrderItem.objects.values("product_id").distinct()
).order_by("title")
```

---

## ⚙️ Performance Optimizations

### 1. Load only specific fields

```python
queryset = Product.objects.only('id', 'title')
```

### 2. Exclude fields

```python
queryset = Product.objects.defer("description")
```

### 3. Join-related models efficiently

```python
queryset = Product.objects.select_related('collection').all()  # One-to-one / ForeignKey
queryset = Product.objects.prefetch_related("promotions").all()  # Many-to-many / reverse FK
```

### Combined example:

```python
queryset = (
    Product.objects.prefetch_related("promotions")
    .select_related("collection")
    .all()
)
```

### For nested relationships:

```python
queryset = (
    Order.objects.select_related("customer")
    .prefetch_related("orderitem_set__product")
    .order_by("-placed_at")[:5]
)
```

---

## 🧮 Aggregation

```python
result = Product.objects.aggregate(Count("id"))
result = Product.objects.aggregate(count=Count("id"))
result = Product.objects.aggregate(count=Count("id"), min_price=Min("unit_price"))
```

### Filter before aggregation

```python
result = Product.objects.filter(collection__id=1).aggregate(
    count=Count("id"), min_price=Min("unit_price")
)
```

### More examplesd

```python
result = OrderItem.objects.filter(product__id=1).aggregate(
    units_sold=Sum("quantity")
)
result = Product.objects.filter(collection__id=3).aggregate(
    max_price=Max("unit_price"),
    min_price=Min("unit_price"),
    avg_price=Avg("unit_price"),
)
```

---

## 🧾 Annotation (Computed Columns)

### 1. Add constants or derived fields

```python
queryset = Customer.objects.annotate(is_new=Value(True))
queryset = Customer.objects.annotate(new_id=F('id') + 1000)
```

### 2. Combine fields

```python
queryset = Customer.objects.annotate(
    full_name=Concat("first_name", Value(" "), "last_name")
)
```

### 3. Count related records

```python
queryset = Customer.objects.annotate(orders_count=Count('order'))
queryset = Collection.objects.annotate(products_count=Count('product'))
```

### 4. Arithmetic using F expressions

```python
from decimal import Decimal
discounted_price = ExpressionWrapper(
    F("unit_price") * Decimal("0.8"),
    output_field=DecimalField()
)
queryset = Product.objects.annotate(discounted_price=discounted_price)
```

### 5. Nested aggregation examples

```python
queryset = Customer.objects.annotate(last_order_id=Max("order__id"))
```

### 6. Total spent per customer

```python
queryset = Customer.objects.annotate(
    total_spent=Sum(
        F('order__orderitem__unit_price') * F('order__orderitem__quantity')
    )
)
```

### 7. Top-selling products

```python
queryset = Product.objects.annotate(
    total_sales=Sum(F("orderitem__unit_price") * F("orderitem__quantity"))
).order_by("total_sales")[:5]
```

---

## 🏷️ Tagged Items (Generic Relations)

```python
# first add manager class
class TaggedItemManager(models.Manager):
    def get_tags_for(self, object_type, object_id):
        # get_form_model is a custom model that exists in ContentType
        content_type = ContentType.objects.get_for_model(object_type)
        queryset = TaggedItem.objects.select_related("tag").filter(
            content_type=content_type, object_id=object_id
        )
        return queryset

# update tag item to add the followign field
objects = TaggedItemManager()

# then hit it
queryset = TaggedItem.objects.get_tags_for(Product, 2)
```

---

## 🧱 Creating & Saving Data

### Option 1: Create, then save

```python
collection = Collection()
collection.title = 'Video games'
collection.featured_product = Product(pk=1)
collection.save()
```

### Option 2: Direct create

```python
collection = Collection.objects.create(title='test', featured_product_id=1)
```

---

## 🗑️ Deleting Data

```python
collection = Collection(pk=11)
collection.delete()

Collection.objects.filter(id__gt=5).delete()
```

---

## 💾 Transactions

Ensure a group of operations succeeds or fails together:

```python
with transaction.atomic():
    order = Order(customer_id=1)
    order.save()

    item = OrderItem(
        order=order,
        product_id=1,
        quantity=1,
        unit_price=10
    )
    item.save()
```

---

## 🧩 Raw SQL

Run raw SQL queries directly:

```python
queryset = Product.objects.raw('SELECT * FROM store_order')
```

Or for non-model queries:

```python
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM store_product WHERE unit_price > %s", [20])
    # cursor.callproc('my_stored_procedure')
```

---

## 🖼️ Rendering a Template

At the end of the view:

```python
return render(request, "hello.html", {"name": "moataz", "tags": []})
```

---

## ✅ Summary

| Concept          | Django Feature                           |
| ---------------- | ---------------------------------------- |
| Filtering        | `filter()`, `Q` objects                  |
| Sorting          | `order_by()`                             |
| Field comparison | `F()`                                    |
| Aggregation      | `aggregate()`                            |
| Computed fields  | `annotate()`                             |
| Joins            | `select_related()`, `prefetch_related()` |
| Transactions     | `transaction.atomic()`                   |
| Raw SQL          | `connection.cursor()`                    |
| CRUD             | `.create()`, `.save()`, `.delete()`      |

---
