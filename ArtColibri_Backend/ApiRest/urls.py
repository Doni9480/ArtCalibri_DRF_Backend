from django.urls import path, include
from rest_framework import routers

from ApiRest.views import CategoryApiView, GalleryApiView, ProductsApiView, LidSaleApiView

router = routers.DefaultRouter()
router.register(r'category', CategoryApiView, basename='category')
router.register(r'gallery', GalleryApiView, basename='gallery')
router.register(r'products', ProductsApiView, basename='products')
router.register(r'order', LidSaleApiView, basename='order')

urlpatterns = [
    path('', include(router.urls)),

]
