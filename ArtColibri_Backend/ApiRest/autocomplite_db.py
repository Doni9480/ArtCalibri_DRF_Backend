import datetime
import pathlib
import random

from django.core.files.base import ContentFile

from ApiRest.models import Category,Product, Gallery, HistoryPrice


class AutoCompliteDB:
    def __init__(self):
        self.path_to_images = pathlib.Path(r'C:\Users\doni\Downloads')
        self.name_list = [i for i in self.path_to_images.iterdir() if '.jpg' in i.name]
        self.number_list = []
        self.cat_list = Category.objects.all()

    @staticmethod
    def randomaizer_date():
        return datetime.datetime(year=2023, month=random.randint(1, 12), day=random.randint(1, 28),
                                 hour=random.randint(1, 23), minute=random.randint(1, 59))

    def randomaizer_product_number(self):
        while True:
            num = random.randint(10000, 19999)
            if not self.number_list.count(num):
                self.number_list.append(num)
                return num
            else:
                continue

    def randomaizer_cat_id(self):
        return self.cat_list[random.randint(0, 7)]

    @staticmethod
    def randomaizer_price():
        return random.randint(1100, 2500)

    @staticmethod
    def randomaizer_description():
        list_text = ['Шар с гелием  Круг, С Днем Рождения , единорог, 46 см.',
                     'Шар с гелием  Фигура, Бутылка шампанского "Love", Черный, 84 см.',
                     'Букет футбольной тематики ребенку на 4 года "Будущий победитель"',
                     'Шар с гелием  Фигура, Вытянутое сердце, Фуше, 56 см.',
                     'Воздушная фигура Радужный единорог, 139 см.',
                     'Шар Фигура ходячий, Сказочный Замок, Принцессы Диснея, Розовый',
                     'Шар Тролли Розочка с гелием, ходячий',
                     'Стойка из шаров "Воздушный единорог"',
                     'Шар с гелием Единорог,  С Днем Рождения!, Ассорти, пастель',
                     'Фонтан из гелиевых шаров для девочки, Золушка',
                     'Фонтан из шаров "Полундра" с пиратским кораблем для мальчика',
                     'Шар с гелием  Футбольный мяч, Белый (005), пастель, 5 ст, 30 см.',
                     'Композиция шаров на день рождения']
        return list_text[random.randint(0, 12)]

    def randomaizer_photo(self):
        photo = self.name_list[random.randint(0, len(self.name_list)-1)]
        return ContentFile(photo.open('rb').read(), photo.name)

    def add_work(self):
        model = Product.objects.create(description=self.randomaizer_description(),
                                       cat_id=self.randomaizer_cat_id(),
                                       product_number=self.randomaizer_product_number(),
                                       slug=self.randomaizer_product_number(),
                                       is_my_work=True,
                                       date_added=self.randomaizer_date())
        return model

    def add_product(self):
        model = Product.objects.create(description=self.randomaizer_description(),
                                       cat_id=self.randomaizer_cat_id(),
                                       product_number=self.randomaizer_product_number(),
                                       slug=self.randomaizer_product_number(),
                                       date_added=self.randomaizer_date())
        return model

    def add_photo(self, key):
        for i in range(5):
            ph = self.randomaizer_photo()
            is_title = True if i == 0 else False
            Gallery.objects.create(product=key,
                                   photo=ph,
                                   is_title=is_title)

    def add_price(self, key):
        active_p = self.randomaizer_price()
        old_p = self.randomaizer_price()
        is_action = True if active_p < old_p else False
        HistoryPrice.objects.create(product=key,
                                    price_active=active_p,
                                    price_old=old_p,
                                    is_action=is_action,
                                    date_added=self.randomaizer_date())

    def run(self):
        for _ in range(40):
            m = self.add_product()
            self.add_photo(m)
            self.add_price(m)
            print(f'{_} |{"*"*_}', end='\r')
        for _ in range(20):
            n = self.add_work()
            self.add_photo(n)
            self.add_price(n)
            print(f'{_} |{"*"*_}', end='\r')


if __name__ == '__main__':
    path_to_images = pathlib.Path(r'C:\Users\doni\Downloads')
    name_list = [str(i.absolute()) for i in path_to_images.iterdir() if '.jpg' in i.name]
    print(name_list)
