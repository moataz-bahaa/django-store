from django.urls import include, path
from rest_framework.routers import SimpleRouter, DefaultRouter

from . import views

router = DefaultRouter()

router.register("products", views.ProductViewset)
router.register("collections", views.CollectionViewset)

urlpatterns = router.urls

# if we have some custom patterns
# urlpatterns = [
#     path("", include(router.urls))
# ]
