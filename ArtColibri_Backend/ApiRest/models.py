from django.db import models


# from django.utils import timezone

def get_category_photo_path(self, filename):
    return f'category_img/{self.slug}/{filename}'


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    title_photo = models.ImageField(upload_to=get_category_photo_path, blank=True, verbose_name='Титулное фото')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='Url')

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)

    class Meta:
        db_table = 'category'
        ordering = ['-id', 'name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        # unique_together = ('field1', 'field2')

    def __str__(self):
        return self.name


class Product(models.Model):
    description = models.CharField(max_length=255, verbose_name='Описание')
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    product_number = models.IntegerField(unique=True, verbose_name='Номер продукта')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='Url')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'product'
        ordering = ['-id', 'date_added', 'product_number']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.product_number}'


class Works(models.Model):
    description = models.CharField(max_length=255, verbose_name='Описание')
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    product_number = models.IntegerField(unique=True, verbose_name='Номер продукта')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='Url')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'my_work'
        ordering = ['-id', 'date_added', 'product_number']
        verbose_name = 'Мой продукт'
        verbose_name_plural = 'Мои продукты'

    def __str__(self):
        return f'{self.product_number}'


class HistoryPrice(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт', blank=True, null=True)
    my_product = models.ForeignKey('Works', on_delete=models.CASCADE, verbose_name='Мой продукт', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'history_price'
        ordering = ['-id', 'date_added', 'price']
        verbose_name = 'История цен'
        verbose_name_plural = 'История цен'

    def __str__(self):
        return f'{self.product}|{self.price}'


def get_upload_path(self, filename):
    if self.product:
        return f'{self.product}/{filename}'
    else:
        return f'{self.my_product}/{filename}'

class Gallery(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт', blank=True, null=True)
    my_product = models.ForeignKey('Works', on_delete=models.CASCADE, verbose_name='Мой Продукт', blank=True, null=True)
    photo = models.ImageField(upload_to=get_upload_path, verbose_name='Фото')
    is_title = models.BooleanField(default=False, verbose_name='Главный постер')

    class Meta:
        db_table = 'gallery'
        ordering = ['-id', 'product']
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галерея'

    def __str__(self):
        return f'{self.photo}'
