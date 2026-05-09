from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

router.register("products", views.ProductViewset)
# router.register("reviews", views.ReviewViewset)
router.register("collections", views.CollectionViewset)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewset, basename='product-reviews')

urlpatterns = router.urls + products_router.urls

# if we have some custom patterns
# urlpatterns = [
#     path("", include(router.urls))
# ]
