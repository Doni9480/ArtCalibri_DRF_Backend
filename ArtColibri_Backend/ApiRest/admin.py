from django.contrib import admin

from .models import Category, Product, Gallery, HistoryPrice, Order, Client, PromoCode


class CategoryAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_display = ('id', 'name', 'slug', 'title_photo')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    ordering = ('-id', 'date_added')
    list_display = ('id', 'product_number', 'is_my_work', 'date_added')
    list_display_links = ('product_number',)
    list_filter = ('date_added', 'cat_id', 'is_my_work')
    prepopulated_fields = {'slug': ('product_number',)}
    list_editable = ('is_my_work',)
    search_fields = ('product_number',)


class GalleryAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_display = ('id', 'product', 'photo', 'is_title')
    list_display_links = ('photo', 'id')
    list_filter = ('product',)
    list_editable = ('is_title',)
    search_fields = ('product', 'id',)


class HistoryPriceAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_display = ('id', 'product', 'price_active', 'price_old', 'is_action', 'date_added')
    list_display_links = ('product',)
    list_filter = ('product', 'date_added', 'is_action')


class ClientAdmin(admin.ModelAdmin):
    ordering = ('-data_created', '-id',)
    list_display = ('id', 'tel', 'data_created',)
    list_display_links = ('tel',)
    list_filter = ('tel', 'data_created')


class OrderAdmin(admin.ModelAdmin):
    ordering = ('-count_prod', 'product_key', '-id',)
    list_display = ('id', 'client', 'product_key', 'count_prod')
    list_display_links = ('client',)
    list_filter = ('client',)


class PromoCodeAdmin(admin.ModelAdmin):
    ordering = ('-data_created', '-id',)
    list_display = ('id', 'title', 'discount', 'data_created')
    list_display_links = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(HistoryPrice, HistoryPriceAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)

