from django.contrib import admin

from .models import Category, Product, Works, Gallery, HistoryPrice


class CategoryAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_display = ('id', 'name', 'slug', 'title_photo')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_display = ('id', 'product_number', 'date_added')
    list_display_links = ('product_number',)
    list_filter = ('date_added', 'cat_id')
    prepopulated_fields = {'slug': ('product_number',)}


class WorksAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_display = ('id', 'product_number', 'date_added')
    list_display_links = ('product_number',)
    list_filter = ('date_added',)
    prepopulated_fields = {'slug': ('product_number',)}


class GalleryAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_display = ('id', 'product', 'my_product', 'photo', 'is_title')
    list_display_links = ('photo', 'id')
    list_filter = ('product',)
    list_editable = ('is_title',)
    search_fields = ('id',)


class HistoryPriceAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_display = ('id', 'product', 'price', 'date_added')
    list_display_links = ('price', 'product')
    list_filter = ('product', 'date_added', 'price')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Works, WorksAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(HistoryPrice, HistoryPriceAdmin)
