from django.db.models import Count
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Gallery, Category, Product, HistoryPrice
from .serialaizer import CategorySerialaizer, GallerySerialaizer, ProductSerialaizer, HistoryPriceSerialaizer


class CatigoryApiView(APIView):

    def get(self, request):
        limit = int(request.GET.get("limit", 0))
        if limit != 0:
            cats = Category.objects.order_by('-id')[:limit]
        else:
            cats = Category.objects.order_by('-id')
        return Response({'categoryes': CategorySerialaizer(cats, many=True).data})


class GalleryApiView(APIView):
    def get(self, request):
        if request.GET.get('limit',5):
            model = Gallery.objects.filter(is_title=True,)[:int(request.GET.get('limit',25))]
        else:
            model = Gallery.objects.filter(is_title=True)
        return Response({'photos': GallerySerialaizer(model, many=True).data})


class CategoryProductsApiView(APIView):

    def get(self, request, cat_product):
        category = Category.objects.get(slug=cat_product)
        products = Product.objects.filter(cat_id__slug=cat_product)
        prices = HistoryPrice.objects.filter(product__in=products).order_by('date_added')
        if request.GET and request.GET.get('title') == 'true':
            gallery = Gallery.objects.filter(product__in=products, is_title=True)
        else:
            gallery = Gallery.objects.filter(product__in=products)
        return Response({'category': CategorySerialaizer(category).data,
                         'products': ProductSerialaizer(products, many=True).data,
                         'prices': HistoryPriceSerialaizer(prices, many=True).data,
                         'gallery': GallerySerialaizer(gallery, many=True).data
                         })


class ProductsApiView(APIView):

    def get(self, request):
        if request.GET and request.GET.get('limit'):
            products = Product.objects.order_by('-date_added')[:int(request.GET.get('limit', 10))]
        else:
            products = Product.objects.order_by('-date_added')
        if request.GET and request.GET.get('action') == 'true':
            prices = HistoryPrice.objects.annotate(num_rows=Count('product')).filter(product__in=products).order_by('date_added')
        else:
            prices = HistoryPrice.objects.filter(product__in=products).order_by('date_added')
        if request.GET and request.GET.get('title') == 'true':
            gallery = Gallery.objects.filter(product__in=products, is_title=True)
        else:
            gallery = Product.objects.filter(product__in=products)
        return Response({'products': ProductSerialaizer(products, many=True).data,
                         'prices': HistoryPriceSerialaizer(prices, many=True).data,
                         'gallery': GallerySerialaizer(gallery, many=True).data
                         })

