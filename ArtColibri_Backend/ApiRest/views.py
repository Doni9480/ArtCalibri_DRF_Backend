from django.db.models import Sum
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Gallery, Category, Product, Order
from .serializer import GallerySerialaizer, ProductSerialaizer, CategorySerializer, OrderSerialaizer


class CategoryApiView(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'

    def get_queryset(self):
        limit = self.request.GET.get('limit')
        if limit and limit.isnumeric():
            count_obj = Category.objects.count()
            if count_obj >= int(limit):
                return Category.objects.all()[:int(limit)]
        return Category.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        get_photo = request.GET.get('get_photo')
        if get_photo is not None and get_photo == 'false':
            my_fields = {'cat': ('id', 'name', 'slug')}
        else:
            my_fields = {'cat': ('id', 'name', 'slug', 'title_photo')}

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'my_fields': my_fields})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={'my_fields': my_fields})
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        my_fields = {'cat': ('id', 'name', 'slug',),
                     'cat_products': True,
                     'product': ('id', 'description', 'slug', 'cat_id', 'photo', 'prices'),
                     'gallery': ('id', 'photo'),
                     'prices': ('id', 'price_active', 'price_old')
                     }

        serializer = self.get_serializer(instance, context={"my_fields": my_fields})
        return Response(serializer.data)


class GalleryApiView(ModelViewSet):
    serializer_class = GallerySerialaizer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        get_title_photo = self.request.GET.get('get_title_photo')
        if get_title_photo == 'true':
            return Gallery.objects.filter(is_title=True)
        return Gallery.objects.all()


class ProductsApiView(ModelViewSet):
    serializer_class = ProductSerialaizer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        limit = self.request.GET.get('limit')
        get_action = self.request.GET.get('get_action')
        if get_action == 'true':
            count_obj = Product.objects.filter(historyprice__is_action=True).count()
            if limit and limit.isnumeric() and count_obj >= int(limit):
                return Product.objects.filter(historyprice__is_action=True)[:int(limit)]
            return Product.objects.filter(historyprice__is_action=True)
        return Product.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        # Тут передаем поля модели
        my_fields = {'product': ('id', 'description', 'cat_id', 'slug', 'photo', 'prices'),
                     'gallery': ('id', 'photo'),
                     'prices': ('id', 'price_active', 'price_old')}

        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'my_fields': my_fields})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={'my_fields': my_fields})
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Тут передаем поля модели
        my_fields = {'product': ('id', 'description', 'slug', 'photo', 'prices'),
                     'gallery': ('id', 'photo'),
                     'all_images': True,
                     'prices': ('id', 'price_active', 'price_old')}

        serializer = self.get_serializer(instance, context={'my_fields': my_fields})
        print(serializer.data, '#' * 100)
        return Response(serializer.data)


class LidSaleApiView(ModelViewSet):
    serializer_class = OrderSerialaizer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        limit = self.request.GET.get('limit')
        get_lid_sale = self.request.GET.get('get_lid_sale')
        if get_lid_sale == 'true':
            count_obj = Order.objects.values('product_key').annotate(count=Sum('count_prod')).order_by('-count').count()
            if limit and limit.isnumeric() and count_obj >= int(limit):
                return Order.objects.values('product_key').annotate(count=Sum('count_prod')).order_by('-count')[
                       :int(limit)]
        return Order.objects.values('product_key').annotate(count=Sum('count_prod')).order_by('-count')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        # Тут передаем поля модели
        my_fields = {'product': ('id', 'description', 'cat_id', 'slug', 'photo', 'prices'),
                     'gallery': ('id', 'photo'),
                     'prices': ('id', 'price_active', 'price_old')}

        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'my_fields': my_fields})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={'my_fields': my_fields})
        return Response({'products': serializer.data})
