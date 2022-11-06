import json
import keyword


lesson_str_1 = """{
        "title": "iPhone X",
        "price": 100,
        "class": "smartphone",
        "location": {
        "address": "город Самара, улица Мориса Тореза, 50",
        "metro_stations": ["Спортивная", "Гагаринская"]
        }
        }
        """

lesson_str_2 = """{
        "title": "Вельш-корги",
        "price": 1000,
        "class": "dogs",
        "location": {
        "address": "сельское поселение Ельдигинское, \
поселок санатория Тишково, 25"
        }
        }
        """


class AttrDict(dict):

    """
    Данный класс позволяет получать ключи словаря как атрибуты
    """

    def __init__(self, d):

        """
        Конструктор словаря берет на вход другой словарь и кладет
        к себе пары ключ:значение
        """

        for key, value in d.items():
            self[key] = value

    def __getattr__(self, item):

        """
        Возвращает ключ словаря как атрибут
        """
        return self[item]


class JSON2Python:

    """
    Класс для создания python-объектов из json c доступом через точку
    """

    def __init__(self, json_obj):

        """
        Чтение json-файла и динамическое добавление атрибутов
        """

        for key, value in json_obj.items():
            if type(value) == dict:
                JSON2Python.dynamic_attr(key, AttrDict(value))
            else:
                JSON2Python.dynamic_attr(key, value)

    @classmethod
    def dynamic_attr(cls, key, value):
        if not keyword.iskeyword(key):
            setattr(cls, key, value)
        else:
            setattr(cls, key + '_', value)


class ColorizedMixin:

    """
    Миксина, добавляющая нам цвета
    Мне не получилось добиться того, чтобы цвет можно было передавать
    при инициализации Advert, но тут я и не понял, нужно ли это
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repr_color_code = 36

    def __repr__(self):
        return f"\033[1;{self.repr_color_code};40m'{self.title} | {self.price}"


class AdvertBase(JSON2Python):

    """
    Класс объявления, унаследованный от JSON2Python
    """

    def __init__(self, json_obj):

        """
        Насколько я понял, нам можно объявить атрибут price не через
        динамическое объявление
        """

        super(AdvertBase, self).__init__(json_obj)
        self.price = json_obj['price']

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError('price cannot be negative value')
        self._price = value

    def __repr__(self):
        return f"{self.title} | {self.price}"


class Advert(ColorizedMixin, AdvertBase):

    """
    Вроде как тут даже получилось сделать такую миксину, что при 
    ее удалении все будет работать, но без подстветки, если я 
    правильно понял
    """

    def __init__(self, json_obj):
        super().__init__(json_obj)


if __name__ == '__main__':
    lesson = json.loads(lesson_str_1, strict=False)
    lesson_ad = Advert(lesson)
    print(lesson_ad.location.address)
    print(lesson_ad.price)
    print(lesson_ad)
