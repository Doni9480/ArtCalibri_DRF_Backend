from django.urls import path, include
from rest_framework import routers

from ApiRest.views import CategoryApiView, GalleryApiView, ProductsApiView, LidSaleApiView, PromoCodeApiView

router = routers.DefaultRouter()
router.register(r'category', CategoryApiView, basename='category')
router.register(r'gallery', GalleryApiView, basename='gallery')
router.register(r'products', ProductsApiView, basename='products')
router.register(r'order', LidSaleApiView, basename='order')
# router.register(r'promocode', PromoCodeApiView, basename='promocode')

urlpatterns = [
    path('promocode/', PromoCodeApiView.as_view(), name='promocode-detail'),
    path('', include(router.urls)),

]
