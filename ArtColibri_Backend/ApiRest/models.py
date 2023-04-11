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
    is_my_work = models.BooleanField(default=False, verbose_name='Наш продукт')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'product'
        ordering = ['-id', 'date_added', 'product_number']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.product_number}'


class HistoryPrice(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    price_active = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    price_old = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Старая Цена')
    is_action = models.BooleanField(default=False, verbose_name='Акция')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def save(self, *args, **kwargs):
        if self.pk:
            old_price_active = HistoryPrice.objects.get(pk=self.pk).price_active
            if self.price_active != old_price_active:
                self.price_old = old_price_active
        super(HistoryPrice, self).save(*args, **kwargs)

    class Meta:
        db_table = 'history_price'
        ordering = ['-id', 'date_added', 'price_active', 'price_old']
        verbose_name = 'История цен'
        verbose_name_plural = 'История цен'

    def __str__(self):
        return f'{self.product}|{self.price_active}'


def get_upload_path(self, filename):
    if self.product:
        return f'{self.product}/{filename}'
    else:
        return f'{self.my_product}/{filename}'


class Gallery(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    photo = models.ImageField(upload_to=get_upload_path, verbose_name='Фото')
    is_title = models.BooleanField(default=False, verbose_name='Главный постер')

    class Meta:
        db_table = 'gallery'
        ordering = ['-id', 'product']
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галерея'

    def __str__(self):
        return f'{self.photo}'


class Client(models.Model):
    tel = models.CharField(max_length=50, verbose_name="Номер телефона")
    promo_code = models.ForeignKey('PromoCode', on_delete=models.CASCADE, blank=True, null=True,
                                   verbose_name='Промокод')
    data_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'сlient'
        ordering = ['-data_created', '-id']
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.tel}'


class Order(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name='Клиент')
    product_key = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    count_prod = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        db_table = 'order'
        ordering = ['-id']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.client}'


class PromoCode(models.Model):
    title = models.CharField(max_length=8, verbose_name='Промокод')
    discount = models.PositiveIntegerField(default=1, verbose_name='Скидка')
    data_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'promo_code'
        ordering = ['-id']
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return f'{self.title}'
