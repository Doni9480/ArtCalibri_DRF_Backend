from django.urls import path

from ApiRest.views import CatigoryApiView, GalleryApiView, CategoryProductsApiView, ProductsApiView

urlpatterns = [
    path('category/', CatigoryApiView.as_view()),
    path('gallery/', GalleryApiView.as_view()),
    path('products/', ProductsApiView.as_view()),
    path('category/<slug:cat_product>', CategoryProductsApiView.as_view()),

]
