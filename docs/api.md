# My Django API Notes

This is a personal reminder file for future return to the project, helping recall how the API part was built.

---

## What was learned here

This project is a small Django REST Framework API for products, collections, and reviews. The main goal was to understand:

- how viewsets work
- how filtering is added
- how pagination is configured
- how nested routes are created
- how to protect delete actions when related data exists

---

## Filters

The filter logic lives in [store/filters.py](../store/filters.py).

### ProductFilter

A `FilterSet` is used for products to filter by:

- `collection_id`
- `unit_price` with `gt` and `lt`

This was useful for learning how DRF filters are connected to a viewset.

Example:

```python
class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            "collection_id": ["exact"],
            "unit_price": ["gt", "lt"],
        }
```

---

## Pagination

The custom pagination class is in [store/pagination.py](../store/pagination.py).

### DefaultPagination

A simple pagination class extends `PageNumberPagination`:

```python
class DefaultPagination(PageNumberPagination):
    page_size = 10
```

This was a good example of making API responses easier to browse in smaller chunks.

---

## Views

The main view logic is in [store/views.py](../store/views.py).

### ProductViewset

This is a main learning example for a `ModelViewSet`.

Key points:

- `queryset = Product.objects.all()`
- `serializer_class = ProductSerailzer`
- search by title and description
- ordering by unit price and last update
- custom filters and pagination

Deleting a product is blocked when it is related to an order item.

### ReviewViewset

This viewset shows how to work with nested resources.

It filters reviews by the current product ID using the URL parameter `product_pk`.

### CollectionViewset

This is useful for learning annotation.

It uses:

```python
Collection.objects.annotate(products_count=Count("products")).all()
```

And it also prevents deleting a collection if it still contains products.

---

## Routing

The routes are in [store/urls.py](../store/urls.py).

The important part is learning nested routers:

- `/products/`
- `/collections/`
- `/products/<product_id>/reviews/`

This helped me understand how parent-child API endpoints are structured.

---

## Quick memory aid

Key reminders:

- filters are added through `filterset_class`
- pagination is attached with `pagination_class`
- searches and ordering use DRF backends
- nested review endpoints are registered with a nested router
- delete actions can be protected manually in the viewset
