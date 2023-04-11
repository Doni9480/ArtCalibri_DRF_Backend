from rest_framework import serializers
from rest_framework.fields import SkipField

from .models import Category, Gallery, Product, HistoryPrice, Order


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'title_photo')

    def to_representation(self, instance):
        my_field_data = self.context.get('my_fields', {'cat': ('id', 'name', 'slug', 'title_photo')})
        fields = self._readable_fields
        data = {}
        for field in fields:
            try:
                if my_field_data:
                    if field.field_name in my_field_data.get('cat'):
                        attribute = field.get_attribute(instance)
                        data[field.field_name] = field.to_representation(attribute)
            except SkipField:
                continue
        if my_field_data.get('cat_products'):
            data['products'] = ProductSerialaizer(Product.objects.filter(cat_id=data.get('id')), many=True,
                                                  context=self.context).data
        return data


class GallerySerialaizer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    cat_slug = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = ('id', 'photo', 'cat_slug', 'product')

    def get_cat_slug(self, obj):
        return obj.product.cat_id.slug

    def to_representation(self, instance):
        my_field_data = self.context.get('gallery_fields', ('id', 'photo', 'cat_slug', 'product'))
        fields = self._readable_fields
        data = {}
        for field in fields:
            try:
                if my_field_data:
                    if field.field_name in my_field_data:
                        attribute = field.get_attribute(instance)
                        data[field.field_name] = field.to_representation(attribute)
            except SkipField:
                continue
        return data


class ProductSerialaizer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    prices = serializers.SerializerMethodField()
    cat_id = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'description', 'cat_id', 'product_number', 'slug', 'photo', 'prices')

    def get_photo(self, obj):
        my_fields_photo = self.context.get('my_fields').get('gallery') if self.context.get('my_fields') else None
        if self.context.get('my_fields'):
            if self.context.get('my_fields').get('all_images'):
                photo = GallerySerialaizer(Gallery.objects.filter(product=obj),
                                           context={'gallery_fields': my_fields_photo}, many=True)
                return photo.data
            else:
                photo = GallerySerialaizer(Gallery.objects.get(product=obj, is_title=True),
                                           context={'gallery_fields': my_fields_photo})
                return photo.data

    def get_prices(self, obj):
        my_fields_price = self.context.get('my_fields').get('prices') if self.context.get('my_fields') else None
        prices = HistoryPriceSerialaizer(HistoryPrice.objects.get(product=obj),
                                         context={'price_fields': my_fields_price})
        return prices.data

    def to_representation(self, instance):
        my_field_data = self.context.get('my_fields')
        fields = self._readable_fields
        data = {}
        for field in fields:
            try:
                if my_field_data:
                    if field.field_name in my_field_data.get('product'):
                        attribute = field.get_attribute(instance)
                        data[field.field_name] = field.to_representation(attribute)
            except SkipField:
                continue
        return data


class HistoryPriceSerialaizer(serializers.ModelSerializer):
    class Meta:
        model = HistoryPrice
        fields = '__all__'

    def to_representation(self, instance):
        my_field_data = self.context.get('price_fields', ('product', 'price', 'date_added'))
        fields = self._readable_fields
        data = {}
        for field in fields:
            try:
                if my_field_data:
                    if field.field_name in my_field_data:
                        attribute = field.get_attribute(instance)
                        data[field.field_name] = field.to_representation(attribute)
            except SkipField:
                continue
        return data


class OrderSerialaizer(serializers.ModelSerializer):
    product_key = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('product_key',)

    def get_product_key(self, obj):
        product = ProductSerialaizer(Product.objects.get(pk=obj.get('product_key')), read_only=True,
                                     context=self.context)
        return product.data

    def to_representation(self, instance):
        data = {
            **self.get_product_key(instance)
        }
        return data
