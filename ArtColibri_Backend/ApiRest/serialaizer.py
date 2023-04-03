from rest_framework import serializers

from .models import Category, Gallery, Product, HistoryPrice, Works


class CategorySerialaizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'title_photo')


class GallerySerialaizer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ('id', 'photo', 'product', 'my_product')


class ProductSerialaizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'description', 'cat_id', 'product_number', 'slug')


class WorksSerialaizer(serializers.ModelSerializer):
    class Meta:
        model = Works
        fields = ('id', 'description', 'cat_id', 'product_number', 'slug')


class HistoryPriceSerialaizer(serializers.ModelSerializer):
    class Meta:
        model = HistoryPrice
        fields = ('id', 'product', 'my_product', 'price', 'date_added')
